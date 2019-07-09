from django.test import TestCase

from ..utils import (
    FuzzyInt, markdown_to_html
)


class TestFuzzyInt(TestCase):

    def test_values(self):
        self.assertNotEqual(4, FuzzyInt(5, 8))
        self.assertEqual(5, FuzzyInt(5, 8))
        self.assertEqual(6, FuzzyInt(5, 8))
        self.assertEqual(7, FuzzyInt(5, 8))
        self.assertEqual(8, FuzzyInt(5, 8))
        self.assertNotEqual(9, FuzzyInt(5, 8))


class TestUtilities(TestCase):

    def test_markdown_to_html(self):
        # Blank text
        for markdown_text in ['', None]:
            self.assertEqual('', markdown_to_html(markdown_text))
        # Italic
        for markdown_text in ['*testing testing*', '_testing testing_']:
            self.assertEqual(
                '<p><em>testing testing</em></p>\n',
                markdown_to_html(markdown_text)
            )
        # Boldface
        for markdown_text in ['**testing testing**', '__testing testing__']:
            self.assertEqual(
                '<p><strong>testing testing</strong></p>\n',
                markdown_to_html(markdown_text)
            )
        # Boldface italic
        for markdown_text in ['**_testing testing_**', '__*testing testing*__']:
            self.assertEqual(
                '<p><strong><em>testing testing</em></strong></p>\n',
                markdown_to_html(markdown_text)
            )
        # Headers
        html = markdown_to_html('# hello\n## hello')
        self.assertEqual('<h1>hello</h1>\n\n<h2>hello</h2>\n', html)
        # Lists
        for markdown_text in ['- hello\n- hello', '* hello\n* hello']:
            self.assertEqual(
                '<ul>\n<li>hello</li>\n<li>hello</li>\n</ul>\n',
                markdown_to_html(markdown_text)
            )
        # Code blocks
        # Fenced-in code with syntax highlighting
        html = markdown_to_html('```python\nHello\n```')
        self.assertEqual(
            '<pre><code>Hello\n</code></pre>\n',
            html
        )
        # Fenced-in code without syntax highlighting
        html = markdown_to_html('```\nHello\n```')
        self.assertEqual(
            '<pre><code>Hello\n</code></pre>\n',
            html
        )
        # Tab-based code block
        html = markdown_to_html('\tHello\n')
        self.assertEqual(
            '<pre><code>Hello\n</code></pre>\n',
            html
        )
        # Links
        # Inline-style link
        html = markdown_to_html('[I am a link](https://www.foo.com)')
        self.assertEqual(
            '<p><a href="https://www.foo.com">I am a link</a></p>\n',
            html
        )
        # Inline-style link with title
        html = markdown_to_html(
            '[I am a link](https://foo.com "Title")'
        )
        self.assertEqual(
            '<p><a href="https://foo.com" title="Title">' +
            'I am a link</a></p>\n',
            html
        )
        # Rerefence-style link with title
        html = markdown_to_html(
            '[I am a link][reference text]\n' +
            '[reference text]:https://foo.com "Title"'
        )
        self.assertEqual(
            '<p><a href="https://foo.com" title="Title">' +
            'I am a link</a></p>\n',
            html
        )
        # Images
        html = markdown_to_html('![alt text](../foo.png "img text")')
        self.assertEqual('<p><img src="../foo.png" alt="alt text" title="img text" /></p>\n', html)
        html = markdown_to_html('![alt text][logo]\n[logo]:../foo.png "img text"')
        self.assertEqual('<p><img src="../foo.png" alt="alt text" title="img text" /></p>\n', html)
