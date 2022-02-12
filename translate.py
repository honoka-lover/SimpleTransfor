from selenium import webdriver


class Translate():
    def __init__(self, source):
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        profile = webdriver.FirefoxProfile()
        self.browser = webdriver.Firefox(options=options, firefox_profile=profile)

        self.browser.get("https://fanyi.youdao.com/")
        self.sentence = ''
        self.src = source
        self.result = ""
        self.len = 0

    def cut_text(self, text, lenth=500):
        text += '\n'
        rst = []
        n = 0
        strings = ''
        for i in text:
            self.len = self.len+1
            strings += i
            if i != '\n':
                continue
            else:
                n = n + 1
                if n < lenth:
                    continue
                else:
                    rst.append(strings)
                    strings = ''
                    n = 0
        if strings:
            rst.append(strings)
        return rst

    def get(self, str):
        self.sentence = ''
        if str:
            self.browser.refresh()
            element = self.browser.find_element_by_id("inputOriginal")
            # element.clear()
            element.send_keys(str)
            self.browser.implicitly_wait(1)
            result = self.browser.find_element_by_id('transTarget').find_elements_by_tag_name('p')

            for i in result:
                self.sentence += i.text + '\n'
        else:
            pass
        return self.sentence


    def trans(self):
        source = self.cut_text(self.src)
        #print(source)
        for i in source:
            self.result += self.get(i)
        return self.result

    def close(self):
        self.browser.close()

if __name__ == '__main__':
    t = Translate('hello\n'
                  'world\n'
                  '你好')
    print(t.trans())
