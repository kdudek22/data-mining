from selenium.webdriver.common.by import By

COOKIE_ACCEPT = (By.ID, 'onetrust-accept-btn-handler')

LISTINGS_GRID = (By.XPATH, '//*[@data-testid="listing-grid"]')

LISTINGS = (By.CSS_SELECTOR, '[data-cy="l-card"]')

LISTING_LINK = (By.TAG_NAME, "a")

LISTINGS_NEXT_PAGE = (By.CSS_SELECTOR, '[data-testid="pagination-forward"]')


LISTING_PARAMETERS = (By.CSS_SELECTOR, '[data-testid="ad-parameters-container"]')
LISTING_PARAMETER = (By.TAG_NAME, "p")
LISTING_PRICE = (By.CSS_SELECTOR, '[data-testid="ad-price-container"]')
LISTING_TITLE = (By.CSS_SELECTOR, '[data-cy="offer_title"]')
LISTING_ID = (By.CLASS_NAME, 'css-ooacec')
LISTING_DESCRIPTION = (By.CLASS_NAME, 'css-19duwlz')