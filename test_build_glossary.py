import unittest

from build_glossary import render, splice

CONTEXT = """# Name

Description.

## Language

### Case

**Case**:
A versioned definition with a `{{task}}` & a **key**.
_Avoid_: test

**Task**:
The public field.
"""


class RenderTest(unittest.TestCase):
    def test_renders_groups_and_terms_without_avoid_lines(self):
        self.assertEqual(
            render(CONTEXT),
            '<section id="glossary"><h2>Glossary</h2>\n'
            "<h3>Case</h3>\n"
            '<dl class="glossary">\n'
            "  <div><dt>Case</dt> <dd>A versioned definition with a "
            "<code>{{task}}</code> &amp; a <strong>key</strong>.</dd></div>\n"
            "  <div><dt>Task</dt> <dd>The public field.</dd></div>\n"
            "</dl>\n"
            "</section>",
        )


class SpliceTest(unittest.TestCase):
    def test_replaces_only_the_text_between_markers(self):
        html = "a<!-- glossary:start -->old<!-- glossary:end -->b"
        self.assertEqual(
            splice(html, "new"),
            "a<!-- glossary:start -->\nnew\n<!-- glossary:end -->b",
        )

    def test_fails_without_markers(self):
        with self.assertRaises(ValueError):
            splice("no markers", "new")


if __name__ == "__main__":
    unittest.main()
