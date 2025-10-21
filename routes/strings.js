const express = require("express");
const fs = require("fs");
const crypto = require("crypto"); // for sha256 hash
const router = express.Router();

let data = []
if (fs.existsSync('storage.json')) {
  data = JSON.parse(fs.readFileSync('storage.json'));
}

router.post('/', (req, res) => {
  const { value } = req.body;

  if (!value) return res.status(400).json({ error: 'Missing "value" field' });
  if (typeof value !== 'string') return res.status(422).json({ error: '"value" must be a string' });

  const sha256_hash = crypto.createHash('sha256').update(value).digest('hex');
  if (data.find((item) => item.id === sha256_hash)) return res.status(409).json({ error: 'String already exists' });

  const properties = {
    length: value.length,
    is_palindrome: value.toLowerCase() === value.toLowerCase().split('').reverse().join(''),
    unique_characters: new Set(value).size,
    word_count: value.trim().split(/\s+/).length,
    sha256_hash,
    character_frequency_map: [...value].reduce((acc, char) => {
      acc[char] = (acc[char] || 0) + 1;
      return acc;
    }, {})
  };

  const newEntry = {
    id: sha256_hash,
    value,
    properties,
    created_at: new Date().toISOString()
  };

  data.push(newEntry);
  fs.writeFileSync('storage.json', JSON.stringify(data, null, 2));

  res.status(201).json(newEntry);
});

router.get('/:string_value', (req, res) => {
  const { string_value } = req.params;
  const entry = data.find((d) => d.value === string_value);
  if (!entry) return res.status(404).json({ error: 'String not found' });
  res.json(entry);
});


// GET /strings with filtering
router.get("/", (req, res) => {
  try {
    let results = data;

    const {
      is_palindrome,
      min_length,
      max_length,
      word_count,
      contains_character,
    } = req.query;

    // Validate query parameters
    if (
      (is_palindrome && !["true", "false"].includes(is_palindrome)) ||
      (min_length && isNaN(min_length)) ||
      (max_length && isNaN(max_length)) ||
      (word_count && isNaN(word_count)) ||
      (contains_character && contains_character.length !== 1)
    ) {
      return res.status(400).json({
        message: "Invalid query parameter values or types",
      });
    }

    // Apply filters
    if (is_palindrome !== undefined) {
      const boolVal = is_palindrome === "true";
      results = results.filter((item) => item.properties.is_palindrome === boolVal);
    }

    if (min_length !== undefined) {
      results = results.filter(
        (item) => item.value.length >= parseInt(min_length)
      );
    }

    if (max_length !== undefined) {
      results = results.filter(
        (item) => item.value.length <= parseInt(max_length)
      );
    }

    if (word_count !== undefined) {
      results = results.filter(
        (item) =>
          item.value.trim().split(/\s+/).length === parseInt(word_count)
      );
    }

    if (contains_character !== undefined) {
      results = results.filter((item) =>
        item.value.toLowerCase().includes(contains_character.toLowerCase())
      );
    }

    // Respond with structured result
    res.status(200).json({
      data: results,
      count: results.length,
      filters_applied: {
        ...(is_palindrome && { is_palindrome: is_palindrome === "true" }),
        ...(min_length && { min_length: parseInt(min_length) }),
        ...(max_length && { max_length: parseInt(max_length) }),
        ...(word_count && { word_count: parseInt(word_count) }),
        ...(contains_character && { contains_character }),
      },
    });
  } catch (error) {
    res.status(500).json({ message: "Server error", error: error.message });
  }
});



/**
 * Utility: interpret natural language query into filters
 */
function parseNaturalLanguage(query) {
  const q = query.toLowerCase();
  const filters = {};

  // Single word check
  if (q.includes("single word")) filters.word_count = 1;

  // Palindromic strings
  if (q.includes("palindromic")) filters.is_palindrome = true;

  // Longer than X characters (regex match)
  const longerMatch = q.match(/longer than (\d+) characters?/);
  if (longerMatch) filters.min_length = parseInt(longerMatch[1]) + 1;

  // Containing letter X
  const containMatch = q.match(/containing the letter ([a-z])/);
  if (containMatch) filters.contains_character = containMatch[1];

  // Contain the first vowel (a simple heuristic)
  if (q.includes("first vowel")) filters.contains_character = "a";

  // Conflicting query: e.g., word_count=1 and word_count=2 at once
  const uniqueKeys = Object.keys(filters);
  if (uniqueKeys.length === 0)
    throw new Error("Unable to parse natural language query");

  return filters;
}

/**
 * Natural language filtering endpoint
 */
router.get("/filter-by-natural-language", (req, res) => {
  try {
    const { query } = req.query;
    if (!query) {
      return res.status(400).json({ message: "Missing query parameter" });
    }

    let parsedFilters;
    try {
      parsedFilters = parseNaturalLanguage(query);
    } catch (error) {
      return res.status(400).json({
        message: "Unable to parse natural language query",
      });
    }

    // Apply filters to data (reuse same logic as /strings)
    let results = data;

    if (parsedFilters.is_palindrome !== undefined) {
      results = results.filter(
        (item) => item.properties.is_palindrome === parsedFilters.is_palindrome
      );
    }

    if (parsedFilters.min_length !== undefined) {
      results = results.filter(
        (item) => item.value.length >= parsedFilters.min_length
      );
    }

    if (parsedFilters.contains_character !== undefined) {
      results = results.filter((item) =>
        item.value
          .toLowerCase()
          .includes(parsedFilters.contains_character.toLowerCase())
      );
    }

    if (parsedFilters.word_count !== undefined) {
      results = results.filter(
        (item) =>
          item.value.trim().split(/\s+/).length === parsedFilters.word_count
      );
    }

    // Respond
    return res.status(200).json({
      data: results,
      count: results.length,
      interpreted_query: {
        original: query,
        parsed_filters: parsedFilters,
      },
    });
  } catch (error) {
    console.error(error);
    return res.status(422).json({
      message: "Query parsed but resulted in conflicting filters",
      error: error.message,
    });
  }
});



router.delete('/:string_value', (req, res) => {
    const { string_value } = req.params;
    const index = data.findIndex((d) => d.value === string_value);
    if (index === -1) return res.status(404).json({ error: 'String not found' });

  data.splice(index, 1);
  fs.writeFileSync('storage.json', JSON.stringify(data, null, 2));
  res.status(204).send();
});

module.exports = router;