"""
A simplified browser tool for OpenManus based on Playwright.
"""

import asyncio
import base64
import json
import os
from typing import Any, Dict, List, Optional, Union

from loguru import logger
from playwright.async_api import async_playwright

from app.tool.base import BaseTool, ToolResult


class BrowserUseTool(BaseTool):
    """
    A simplified browser tool for OpenManus using Playwright.
    """

    name: str = "browser_use"
    description: str = "Use a browser to navigate and interact with web pages."
    
    # 定义 Pydantic 字段
    browser: Optional[Any] = None
    context: Optional[Any] = None
    page: Optional[Any] = None
    _playwright: Optional[Any] = None
    
    def __init__(self):
        super().__init__()
    
    async def _ensure_browser(self):
        """Ensure browser is initialized."""
        if self.browser is None:
            self._playwright = await async_playwright().start()
            self.browser = await self._playwright.chromium.launch(headless=False)
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()
    
    async def execute(self, action: str, url: Optional[str] = None, **kwargs) -> ToolResult:
        """
        Execute a browser action.
        
        Args:
            action: The action to perform (goto, screenshot, click, type, etc.)
            url: The URL to navigate to (for goto action)
            **kwargs: Additional parameters for the action
            
        Returns:
            ToolResult: The result of the action
        """
        try:
            await self._ensure_browser()
            
            if action == "goto":
                if not url:
                    return ToolResult(error="URL is required for goto action")
                await self.page.goto(url)
                return ToolResult(output=f"Navigated to {url}")
            
            elif action == "screenshot":
                screenshot_bytes = await self.page.screenshot()
                base64_image = base64.b64encode(screenshot_bytes).decode('utf-8')
                return ToolResult(output="Screenshot taken", base64_image=base64_image)
            
            elif action == "click":
                selector = kwargs.get("selector")
                if not selector:
                    return ToolResult(error="Selector is required for click action")
                await self.page.click(selector)
                return ToolResult(output=f"Clicked on {selector}")
            
            elif action == "type":
                selector = kwargs.get("selector")
                text = kwargs.get("text")
                if not selector or text is None:
                    return ToolResult(error="Selector and text are required for type action")
                await self.page.fill(selector, text)
                return ToolResult(output=f"Typed '{text}' into {selector}")
            
            elif action == "get_text":
                selector = kwargs.get("selector")
                if not selector:
                    return ToolResult(error="Selector is required for get_text action")
                text = await self.page.text_content(selector)
                return ToolResult(output=text)
            
            elif action == "get_current_state":
                # Get current page state
                url = self.page.url
                title = await self.page.title()
                
                # Take screenshot
                screenshot_bytes = await self.page.screenshot()
                base64_image = base64.b64encode(screenshot_bytes).decode('utf-8')
                
                # Get page dimensions
                dimensions = await self.page.evaluate("""() => {
                    return {
                        scrollHeight: document.documentElement.scrollHeight,
                        scrollTop: document.documentElement.scrollTop,
                        clientHeight: document.documentElement.clientHeight
                    }
                }""")
                
                pixels_above = dimensions["scrollTop"]
                pixels_below = dimensions["scrollHeight"] - dimensions["clientHeight"] - pixels_above
                
                state = {
                    "url": url,
                    "title": title,
                    "pixels_above": pixels_above,
                    "pixels_below": pixels_below,
                    "tabs": [{"url": url, "title": title}]
                }
                
                return ToolResult(
                    output=json.dumps(state),
                    base64_image=base64_image
                )
            
            else:
                return ToolResult(error=f"Unknown action: {action}")
                
        except Exception as e:
            logger.error(f"Browser error: {str(e)}")
            return ToolResult(error=f"Browser error: {str(e)}")
    
    async def cleanup(self):
        """Clean up browser resources."""
        try:
            if self.browser:
                await self.browser.close()
            if self._playwright:
                await self._playwright.stop()
            self.browser = None
            self.context = None
            self.page = None
            self._playwright = None
        except Exception as e:
            logger.error(f"Error cleaning up browser: {str(e)}")
