from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


elements = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"div.categoryBoardsDroppableArea > div[data-rbd-draggable-context-id] > div[role=\"button\"]")))
        for element in elements:
            ActionChains(driver).move_to_element(element).perform()
