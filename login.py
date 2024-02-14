import asyncio
from pyppeteer import launch


async def indeed_login():
    # Launch the browser
    browser = await launch(headless=False)  # headless=False to see the browser actions
    page = await browser.newPage()

    # Navigate to Indeed's login page
    await page.goto('https://secure.indeed.com/account/login')

    # Click on the "Sign in with Google" button
    await page.click('#login-google-button')

    # Wait for the new page (Google login page) to load
    await page.waitForNavigation()

    # You might need to wait for the selector that identifies the email input field on the Google login page
    await page.waitForSelector('input[type="email"]', {'visible': True})

    # Fill in the Google email and press Enter
    await page.type('input[type="email"]', 'maldonadoike@gmail.com')
    await page.keyboard.press('Enter')

    # Wait for the password field to appear
    await page.waitForSelector('input[type="password"]', {'visible': True})

    # Fill in the password and press Enter
    await page.type('input[type="password"]', 'your_password')
    await page.keyboard.press('Enter')

    # Wait for the navigation after login
    await page.waitForNavigation()

    print("Logged in successfully!")

    # Continue with your actions after login...

    # Close the browser
    await browser.close()


# Run the async function
asyncio.get_event_loop().run_until_complete(indeed_login())
