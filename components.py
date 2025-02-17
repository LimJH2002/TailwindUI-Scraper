import os
import re
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_component_structure(driver):
    # Find all main sections (Application UI, Marketing, Ecommerce)
    main_sections = driver.find_elements(
        By.CSS_SELECTOR, "section[id^='product-'].scroll-mt-28"
    )
    structure = []

    for main_section in main_sections:
        try:
            # Get main section title
            main_title = main_section.find_element(By.TAG_NAME, "h2").text

            # Find all subsections within this main section
            subsections = main_section.find_elements(By.TAG_NAME, "section")
            section_data = {"main_title": main_title, "subsections": []}

            for subsection in subsections:
                try:
                    # Get subsection title from h3
                    subsection_title = subsection.find_element(By.TAG_NAME, "h3").text

                    # Get all links in this subsection
                    links = subsection.find_elements(By.TAG_NAME, "a")
                    link_data = []

                    for link in links:
                        try:
                            href = link.get_attribute("href")
                            text = link.text
                            if href and text:  # Only add if both exist
                                link_data.append({"text": text, "href": href})
                        except:
                            continue

                    if link_data:  # Only add subsection if it has links
                        section_data["subsections"].append(
                            {"subsection_title": subsection_title, "links": link_data}
                        )
                except:
                    continue

            structure.append(section_data)

        except Exception as e:
            print(f"Error processing main section: {str(e)}")
            continue

    return structure


def save_structure_to_file(structure, filename="tailwind_structure.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for main_section in structure:
            # Write main section title
            f.write(f"\n{main_section['main_title']}\n")
            f.write("=" * 50 + "\n\n")

            # Write subsections
            for subsection in main_section["subsections"]:
                f.write(f"{subsection['subsection_title']}\n")
                f.write("-" * 40 + "\n")

                # Write links
                for i, link in enumerate(subsection["links"], 1):
                    f.write(f"{i}. {link['text']}\n")
                    f.write(f"   URL: {link['href']}\n")
                f.write("\n")


def visit_component_urls(urls_file):
    driver = login(webdriver.Chrome())
    wait = WebDriverWait(driver, 10)

    # Add a set to track unique code snippets
    seen_code = set()
    duplicate_count = 0
    max_duplicates = 3  # Stop after this many consecutive duplicates

    try:
        with open(urls_file, "r", encoding="utf-8") as f:
            content = f.read()
            current_main_section = None
            current_subsection = None
            current_component_title = None
            previous_line = ""

            lines = content.split("\n")
            for line in lines:
                if "=" * 10 in line and previous_line:
                    current_main_section = previous_line.strip()
                    os.makedirs(
                        os.path.join("components", current_main_section), exist_ok=True
                    )

                elif "-" * 10 in line and previous_line:
                    current_subsection = previous_line.strip()
                    os.makedirs(
                        os.path.join(
                            "components", current_main_section, current_subsection
                        ),
                        exist_ok=True,
                    )

                elif line.strip().startswith(tuple("123456789")):
                    current_component_title = line.split(".", 1)[1].strip()
                    os.makedirs(
                        os.path.join(
                            "components",
                            current_main_section,
                            current_subsection,
                            current_component_title,
                        ),
                        exist_ok=True,
                    )

                elif "URL:" in line:
                    url = line.split("URL:")[1].strip()
                    print(f"\nVisiting: {url}")

                    try:
                        driver.get(url)
                        wait.until(
                            EC.presence_of_element_located(
                                (By.CSS_SELECTOR, "section[id^='component-']")
                            )
                        )

                        component_sections = driver.find_elements(
                            By.CSS_SELECTOR, "section[id^='component-']"
                        )

                        for section in component_sections:
                            section_id = section.get_attribute("id")
                            title_link = section.find_element(
                                By.CSS_SELECTOR, f"a[href='#{section_id}']"
                            )
                            title = title_link.text

                            print(f"Component ID: {section_id}")
                            print(f"Title: {title}")

                            code_tab = section.find_element(
                                By.XPATH, ".//button[.//span[contains(text(), 'Code')]]"
                            )
                            code_tab.click()
                            time.sleep(1)

                            code = get_component_code(driver, section_id)

                            if code:
                                # Check if we've seen this code before
                                if code in seen_code:
                                    duplicate_count += 1
                                    print(
                                        f"WARNING: Duplicate code detected ({duplicate_count}/{max_duplicates})"
                                    )

                                    if duplicate_count >= max_duplicates:
                                        print(
                                            "\nToo many consecutive duplicates detected. Stopping script."
                                        )
                                        return
                                else:
                                    duplicate_count = (
                                        0  # Reset counter when unique code is found
                                    )
                                    seen_code.add(code)

                                    safe_title = re.sub(r"[^a-zA-Z0-9]", "", title)
                                    filepath = os.path.join(
                                        "components",
                                        current_main_section,
                                        current_subsection,
                                        current_component_title,
                                        f"{safe_title}.jsx",
                                    )

                                    with open(filepath, "w", encoding="utf-8") as f:
                                        f.write(code)
                                    print(f"Saved to: {filepath}")

                            time.sleep(2)

                    except Exception as e:
                        print(f"Error loading component: {str(e)}")
                        continue

                previous_line = line

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()


def login(driver):
    driver.get("https://tailwindui.com/login")
    wait = WebDriverWait(driver, 20)

    # Wait for content to load
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))

    # Find the login form
    form = driver.find_element(By.TAG_NAME, "form")

    # Fill in the form
    form.find_element(By.ID, "email").send_keys(os.getenv("TAILWIND_UI_EMAIL"))
    form.find_element(By.ID, "password").send_keys(os.getenv("TAILWIND_UI_PASSWORD"))
    time.sleep(1)  # Wait for 2 seconds before submitting

    # Submit the form
    form.submit()

    wait.until(EC.presence_of_element_located((By.TAG_NAME, "h2")))

    return driver


def get_component_code(driver, section_id):
    try:
        # First, locate the specific section
        section = driver.find_element(By.CSS_SELECTOR, f"section[id='{section_id}']")

        # Find all buttons in the section and look for the one with Code text
        buttons = section.find_elements(By.TAG_NAME, "button")
        code_tab = None
        for button in buttons:
            if "Code" in button.text:
                code_tab = button
                break

        if not code_tab:
            raise Exception("Code tab not found")

        # Click the code tab
        driver.execute_script("arguments[0].click();", code_tab)
        time.sleep(1)  # Wait for code panel to open

        # Wait for code block to be visible
        wait = WebDriverWait(driver, 10)
        code_block = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, f"section[id='{section_id}'] pre code")
            )
        )

        # Get the code content
        code_content = code_block.get_attribute("textContent")

        if not code_content:
            raise Exception("No code content found")

        return code_content.strip()

    except Exception as e:
        print(f"Error getting code for section {section_id}: {str(e)}")
        return None


def save_component_code(code, title, output_dir="components"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Sanitize the title for filename
    filename = re.sub(r"[^a-zA-Z0-9]", "", title)
    filepath = os.path.join(output_dir, f"{filename}.jsx")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"Saved code to: {filepath}")


def main():
    driver = webdriver.Chrome()

    try:
        # Navigate to components page
        driver.get("https://tailwindui.com/components")
        wait = WebDriverWait(driver, 10)

        # Wait for content to load
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h2")))

        # Get the structure
        structure = get_component_structure(driver)

        # Save to file
        save_structure_to_file(structure, "tailwind_components_structure.txt")

        # Visit component URLs
        visit_component_urls("tailwind_components_structure.txt")

    except TimeoutException:
        print("Timed out waiting for content to load")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
