"""Use one numeric display format for full calendar dates in every language."""
import re

MONTHS = {name: f'{number:02}' for number, name in enumerate(
    ('JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'), 1
)}


def normalize_dates(html):
    html = re.sub(
        r'(<time\b[^>]*\bdatetime="(\d{4}-\d{2}-\d{2})"[^>]*>).*?(</time>)',
        lambda match: match[1] + match[2] + match[3],
        html,
        flags=re.S,
    )
    # Convert abbreviated date labels in visible text, preserving URLs and attributes.
    def label(match):
        text = re.sub(
            r'\b(\d{1,2}) (JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC) (\d{4})\b',
            lambda date: f'{date[3]}-{MONTHS[date[2]]}-{int(date[1]):02}', match[1],
        )
        text = re.sub(
            r'\b(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC) (\d{4})\b',
            lambda date: f'{date[2]}-{MONTHS[date[1]]}', text,
        )
        return '>' + text + '<'
    return re.sub(r'>([^<>]+)<', label, html)
