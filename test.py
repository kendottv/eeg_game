import csv
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome");pg=b.new_page(viewport={"width":1000,"height":760},accept_downloads=True)
    pg.goto("file:///workspace/eeg_game/index.html");pg.wait_for_timeout(500)
    pg.screenshot(path="shots/1_start.png")
    pg.evaluate("__CFG.gng.main={n:8,nogo:2};__CFG.itemCapMs=300")
    pg.fill("#pid","P01");pg.click("#next");pg.screenshot(path="shots/2_mode_select.png")
    pg.click("[data-r=seg1]");pg.screenshot(path="shots/3_game1_guide.png");pg.click("#go")
    pg.screenshot(path="shots/4_game1_question.png");pg.click("[data-k='1']")
    pg.wait_for_selector("text=遊戲二",timeout=15000);pg.screenshot(path="shots/5_game2_guide.png");pg.click("#go")
    pg.wait_for_selector("[data-s=go]",timeout=10000);pg.screenshot(path="shots/6_game2_stim.png");pg.wait_for_timeout(250);pg.keyboard.press("Space")
    with pg.expect_download(timeout=30000) as d: pass
    d.value.save_as("shots/sample.csv");pg.wait_for_timeout(300);pg.screenshot(path="shots/7_end.png")
    b.close()
rows=list(csv.DictReader(open("shots/sample.csv",encoding="utf-8-sig")))
hits=[r for r in rows if r["game"]=="G2_gonogo" and r["item_type"]=="go" and r["response"]=="press"]
print(len(rows),"rows; correct Go presses:",[(r["item_no"],r["rt_ms"],r["correct"]) for r in hits])
assert hits and float(hits[0]["rt_ms"])>0 and hits[0]["correct"]=="1"; print("GO RT TEST PASS")
# enableGame2=false path
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome");pg=b.new_page(accept_downloads=True)
    pg.goto("file:///workspace/eeg_game/index.html");pg.evaluate("__CFG.enableGame2=false;__CFG.itemCapMs=200")
    pg.fill("#pid","P02");pg.click("#next");pg.click("[data-r=seg2]");pg.click("#go")
    with pg.expect_download(timeout=20000) as d: pass
    d.value.save_as("shots/sample_nogame2.csv");assert pg.locator("text=完成，謝謝").count()>0;b.close()
r2=list(csv.DictReader(open("shots/sample_nogame2.csv",encoding="utf-8-sig")))
assert len(r2)==15 and all(r["game"]=="G1_comprehension" for r in r2) and list(r2[0].keys())==list(rows[0].keys())
print("ENABLEGAME2=false PASS:",len(r2),"rows")
