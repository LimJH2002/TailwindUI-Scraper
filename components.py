from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_component_structure(driver):
    # Find all main sections (Application UI, Marketing, Ecommerce)
    main_sections = driver.find_elements(By.CSS_SELECTOR, "section[id^='product-']")
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

        print("Structure has been saved to tailwind_components_structure.txt")

    except TimeoutException:
        print("Timed out waiting for content to load")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
