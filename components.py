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

    try:
        with open(urls_file, "r", encoding="utf-8") as f:
            content = f.read()
            current_main_section = None
            current_subsection = None
            current_component_title = None

            # Extract URLs using basic string parsing
            lines = content.split("\n")
            for line in lines:
                if "=" * 10 in line:
                    # This is a main section
                    current_main_section = previous_line.strip()
                    os.makedirs(
                        os.path.join("components", current_main_section), exist_ok=True
                    )
                elif "-" * 10 in line:
                    # This is a subsection
                    current_subsection = previous_line.strip()
                    os.makedirs(
                        os.path.join(
                            "components", current_main_section, current_subsection
                        ),
                        exist_ok=True,
                    )
                elif line.strip().startswith(tuple("123456789")):
                    # This is a component title line (starts with a number)
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

                    # Visit the URL
                    driver.get(url)

                    try:
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
                            print(f"Title: {title}\n")

                            # Click the code tab first
                            code_tab = section.find_element(
                                By.XPATH, ".//button[.//span[contains(text(), 'Code')]]"
                            )
                            code_tab.click()
                            time.sleep(1)

                            # Get the code
                            code = get_component_code(driver, section_id)

                            if code:
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

                    except TimeoutException:
                        print("Timeout waiting for component to load")
                        continue

                    except Exception as e:
                        print(f"Error loading component: {str(e)}")
                        continue

                # Store previous line for section detection
                previous_line = line

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()


def login(driver):
    driver.get("https://tailwindui.com/login")
    wait = WebDriverWait(driver, 10)

    # Wait for content to load
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))

    # Find the login form
    form = driver.find_element(By.TAG_NAME, "form")

    # Fill in the form
    form.find_element(By.ID, "email").send_keys(os.getenv("TAILWIND_UI_EMAIL"))
    form.find_element(By.ID, "password").send_keys(os.getenv("TAILWIND_UI_PASSWORD"))

    # Submit the form
    form.submit()

    wait.until(EC.presence_of_element_located((By.TAG_NAME, "h2")))

    return driver


def get_component_code(driver, section_id):
    try:
        # Find the corresponding copy button within the section
        copy_button = driver.find_element(
            By.CSS_SELECTOR,
            f"section[id='{section_id}'] button.group.relative.ml-2.hidden.size-9",
        )

        # Click copy button
        copy_button.click()
        time.sleep(1)

        # Execute JavaScript to get clipboard content
        clipboard_content = driver.execute_script(
            "return document.querySelector('pre code').textContent"
        )

        return clipboard_content

    except Exception as e:
        print(f"Error getting code: {str(e)}")
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
