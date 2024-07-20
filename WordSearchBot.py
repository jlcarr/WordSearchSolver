from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def build_trie(wordlist):
    trie = dict()
    for word in wordlist:
        curr = trie
        for c in word.upper():
            if c not in curr:
                curr[c] = dict()
            curr = curr[c]
        if 'END' not in curr:
            curr['END'] = word
    return trie

def wordsearch(grid, wordlist, wrap=False, backwards=True):
    trie = build_trie(wordlist)
    nx,ny = len(grid),len(grid[0])
    result = dict()
    for i in range(nx):
        for j in range(ny):
            for di in [-1,0,1]:
                dj_options = [-1,0,1] if backwards else [0,1]
                for dj in dj_options:
                    if di == 0 and dj == 0:
                        continue
                    ip,jp = i,j
                    curr = trie
                    c = grid[i][j]
                    while c in curr:
                        curr = curr[c]
                        if 'END' in curr:
                            w = curr['END']
                            if w not in result:
                                result[w] = set()
                            if w != w[::-1] or ((ip, jp), (-di,-dj)) not in result[w]: # filter palindromes
                                result[w].add(((i,j), (di,dj)))
                        ip += di
                        jp += dj
                        if not ((0 <= ip < len(grid)) and (0 <= jp < len(grid[0]))):
                            if wrap:
                                ip %= len(grid)
                                jp %= len(grid)
                            else:
                                break
                        c = grid[ip][jp]
    return result


def solve(url, wordlist=None):
	browser = webdriver.Firefox()
	browser.get(url)

	wordlist_xpath = "//div[contains(@class, 'words')]"
	WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, wordlist_xpath)))
	wordlist_element = browser.find_element(By.XPATH, wordlist_xpath)

	if wordlist is None:
		wordlist = [w.text for w in wordlist_element.find_elements(By.XPATH, ".//*")]

	grid_xpath = "//div[contains(@class, 'grid')]"
	grid_element = browser.find_element(By.XPATH, grid_xpath)
	letter_elements = grid_element.find_elements(By.XPATH, ".//*")
	letter_elements = [[letter_elements[10*i+j] for j in range(10)] for i in range(len(letter_elements)//10)]

	grid = [[c.text for c in row] for row in letter_elements]
	
	solution = wordsearch(grid, wordlist)

	actions = ActionChains(browser)

	for word in wordlist:
		if word not in solution:
			print(f"- '{word}' NOT FOUND")
			continue
		locations = solution[word]
		print(f"- '{word}' found {len(locations)} times")
		
		xy, d = locations.pop()
		first_element = letter_elements[xy[0]][xy[1]]
		try:
			actions.move_to_element(first_element).perform()
		except:
			browser.execute_script("arguments[0].scrollIntoView(true);", first_element)
		print(f'    - Start letter {first_element.text}')
		last_element = letter_elements[xy[0] + d[0]*(len(word)-1)][xy[1] + d[1]*(len(word)-1)]
		try:
			actions.move_to_element(last_element).perform()
		except:
			browser.execute_script("arguments[0].scrollIntoView(true);", last_element)
		print(f'    - Last letter {last_element.text}')

		actions.drag_and_drop(first_element, last_element).perform()

		
	return browser



if __name__ == '__main__':
	solve('https://wordnerd.co/impossiblewordsearch/')
	#solve('https://wordnerd.co/findthefox/', wordlist=['FOX'])

