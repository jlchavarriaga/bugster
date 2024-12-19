def generate_playwright_test(session_id: str, events: List[Dict]) -> str:
    """
    Genera un script de prueba en Playwright basado en los eventos de una historia.
    """
    script = f"""import {{ test, expect }} from '@playwright/test';

test.describe('Session {session_id}', () => {{
    test('User Story', async ({{
        page
    }}) => {{
"""
    for event in events:
        properties = event["properties"]
        if properties["eventType"] == "click":
            script += f"""        await page.click('{properties["elementAttributes"].get("class", "")}');\n"""
        elif properties["eventType"] == "navigate":
            script += f"""        await page.goto('{properties["$current_url"]}');\n"""
    script += """    });
});
"""
    return script
