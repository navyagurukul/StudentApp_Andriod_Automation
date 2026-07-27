from appium.webdriver.common.appiumby import AppiumBy
import time

class PermissionHandler:

    def __init__(self, driver):
        self.driver = driver

    def allow_notifications(self):
        self._click_allow_buttons(["Allow", "ALLOW", "WHILE USING THE APP", "Allow notifications"])

    def allow_microphone(self):
        self._click_allow_buttons(["While using the app", "Allow", "ALLOW", "Record audio"])

    def handle_all_permissions(self):

        print("\n===== HANDLING PERMISSIONS =====")

        self.allow_notifications()
        time.sleep(1)

        self.allow_microphone()
        time.sleep(1)

        print("Permissions handled\n")

    def _click_allow_buttons(self, texts):

        for _ in range(5):  # retry loop

            for text in texts:

                try:
                    btn = self.driver.find_element(
                        AppiumBy.XPATH,
                        f"//*[@text='{text}']"
                    )
                    btn.click()
                    print(f"Clicked permission: {text}")
                    time.sleep(1)
                    return True

                except:
                    continue

            time.sleep(1)

        print("No permission popup found")
        return False