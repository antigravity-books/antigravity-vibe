import os
import time
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_product_data(driver, brand_name, limit=10):
    products = []
    
    # Wait for the products to load
    time.sleep(3)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find all product items
    items = soup.find_all('li', class_='prod_item')
    
    for item in items:
        # Check if ad
        class_list = item.get('class', [])
        if 'ad_item' in class_list or 'ad' in class_list or 'product-pot' in class_list:
            continue
            
        # Get product name
        name_tag = item.select_one('.prod_name a')
        if not name_tag:
            name_tag = item.select_one('.prod_info_group .prod_name a')
            if not name_tag:
                continue
                
        name = name_tag.text.strip()
        
        # Get specs
        spec_list = item.select_one('.spec_list')
        # 줄바꿈 및 불필요한 공백 제거
        specs = " ".join(spec_list.text.split()) if spec_list else '사양 없음'
        
        # Determine if it's discontinued or out of stock based on price or text
        price_sect = item.select_one('.price_sect')
        price_str = price_sect.text.strip() if price_sect else ''
        if '단종' in price_str or '일시품절' in price_str or '품절' in price_str:
            continue
            
        price_tag = item.select_one('.price_sect strong')
        price = price_tag.text.strip() if price_tag else '가격 없음'
        
        # Record product
        products.append({
            '크롤링_시간': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '제조사': brand_name,
            '상품명': name,
            '사양': specs,
            '가격': price
        })
        
        if len(products) >= limit:
            break
            
    return products

def main():
    print("[INFO] Danawa crawler start...")
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    print("[INFO] Initializing browser...")
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        url = "https://search.danawa.com/dsearch.php?query=43인치+모니터"
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        
        # wait for initial load
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.prod_item')))
        time.sleep(2)
        
        all_products = []
        
        # --- 삼성전자 추출 ---
        print("[INFO] Filtering Samsung products...")
        brand_labels = driver.find_elements(By.CSS_SELECTOR, 'label.srch_lb')
        samsung_clicked = False
        for label in brand_labels:
            if '삼성전자' in label.text:
                driver.execute_script("arguments[0].click();", label)
                samsung_clicked = True
                break
                
        if not samsung_clicked:
            print("[ERROR] Could not find Samsung filter.")
        else:
            time.sleep(4) # wait ajax processing
            samsung_products = get_product_data(driver, "삼성전자", limit=10)
            print(f"[SUCCESS] Extracted {len(samsung_products)} Samsung products.")
            all_products.extend(samsung_products)
        
        # --- 원상복구 ---
        print("[INFO] Resetting filter...")
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.prod_item')))
        time.sleep(2)
        
        # --- LG전자 추출 ---
        print("[INFO] Filtering LG products...")
        brand_labels = driver.find_elements(By.CSS_SELECTOR, 'label.srch_lb')
        lg_clicked = False
        for label in brand_labels:
            if 'LG전자' in label.text:
                driver.execute_script("arguments[0].click();", label)
                lg_clicked = True
                break
                
        if not lg_clicked:
            print("[ERROR] Could not find LG filter.")
        else:
            time.sleep(4) # wait ajax processing
            lg_products = get_product_data(driver, "LG전자", limit=10)
            print(f"[SUCCESS] Extracted {len(lg_products)} LG products.")
            all_products.extend(lg_products)
        
        # --- 결과 저장 ---
        if all_products:
            df = pd.DataFrame(all_products)
            
            # 현재 스크립트 실행 디렉토리(프로젝트 루트) 기준 Scraping_Result 생성
            work_dir = os.getcwd()
            save_dir = os.path.join(work_dir, "Scraping_Result")
            os.makedirs(save_dir, exist_ok=True)
            
            today_str = datetime.now().strftime('%Y%m%d')
            filename = f"danawa_43inch_monitors_{today_str}.csv"
            save_path = os.path.join(save_dir, filename)
            
            df.to_csv(save_path, index=False, encoding='utf-8-sig')
            print(f"[SUCCESS] Data saving completed: {save_path}")
        else:
            print("[WARN] No products extracted.")
            
    except Exception as e:
        print(f"[ERROR] Exception occurred: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
