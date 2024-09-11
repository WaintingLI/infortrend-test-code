from selenium.webdriver.support.ui import Select
#使用Selenium Module中的 Select Module


        select3 = Select(driver.find_element(By.ID,"input-shipping-address"))
        #select3.select_by_index(0)
        #print("select3.options[1].text , vaule=",select3.options[1].text,select3.options[1].get_attribute("value"),type(select3.options[1].get_attribute("value")))
        
        #for op in select3.options:
        #    print("op.text =",op.text)
        #    print("op.value_of_css_property()", op.get_attribute("value"))
        
        # select by visible text
        select3.select_by_visible_text(select3.options[1].text)
        # select by value
        select3.select_by_value(select3.options[1].get_attribute("value"))
        
        
        
#====
    '''
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR,".form-check"))
    )
    #因為返回清單，將所有元素都案一遍
    for cks in element:
        cks.click()
    '''