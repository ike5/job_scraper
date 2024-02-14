import asyncio
from pyppeteer import launch
import pandas as pd
import os


async def start():
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")
    job_you_want = input("What job would you like?")
    job_filename = "test"
    user_data_dir = '/Users/ike/Library/Application Support/Google/Chrome'
    browser = await launch(executablePath='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                           headless=False, userDataDir=user_data_dir)  # headless=False to see the browser
    page = await browser.newPage()
    await page.goto('https://www.indeed.com')
    await page.waitForSelector('#text-input-what')
    await page.waitForSelector('#text-input-where')
    await page.type('#text-input-what', job_you_want)
    await clear_and_type(page, '#text-input-where', 'USA')
    await page.click('button[type="submit"]')
    await page.waitForNavigation()

    jobs_data = []
    while True:  # Loop through pages
        job_listings = await page.querySelectorAll('.resultContent')
        for job in job_listings:
            title_element = await job.querySelector('h2.jobTitle span[title]')
            title = await (await title_element.getProperty('textContent')).jsonValue() if title_element else 'N/A'

            company_element = await job.querySelector('[data-testid="company-name"]')
            company = await (await company_element.getProperty('textContent')).jsonValue() if company_element else 'N/A'

            location_element = await job.querySelector('div.company_location')
            location = await (
                await location_element.getProperty('textContent')).jsonValue() if location_element else 'N/A'

            # Append a dictionary with job details to the list
            jobs_data.append({'title': title, 'company': company, 'location': location})

        next_button = await page.querySelector('[data-testid="pagination-page-next"]')
        if next_button and not await page.evaluate('(button) => button.getAttribute("aria-disabled")', next_button):
            await next_button.click()
            await page.waitForNavigation({'waitUntil': 'networkidle0'})  # Wait for the next page to load completely
        else:
            break  # No more pages

    # Create a DataFrame from the list of job data
    df = pd.DataFrame(jobs_data)

    # Save the DataFrame as a markdown file
    df.to_markdown(f'{job_filename}.md', index=False)

    await browser.close()


async def clear_and_type(page, selector, newText):
    # Focus on the element
    await page.focus(selector)

    # Clear the field using JavaScript
    await page.evaluate(f"""document.querySelector('{selector}').value = ''""")

    # Type the new text
    await page.type(selector, newText)


if __name__ == '__main__':
    asyncio.run(start())
