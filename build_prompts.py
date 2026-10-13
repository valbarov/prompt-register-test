"""Builds prompts.json: 50 tasks x 3 language registers (plain, normal, ornate).

Rule for every task: the three variants carry the same facts, the same conditions, and the same output
format. Only the wording changes. Data the user would paste (order notes, tickets, record lists) is
identical across registers; the wording around it changes. Math problems change as a whole, because the
whole problem is the user's own text.

Families:
  math       10 multi-step word problems, numeric answer
  extract    10 order notes -> JSON with fixed keys (instruction in register, note fixed)
  classify   10 support tickets -> one of 4 labels (instruction in register, ticket fixed)
  filter     10 record lists -> filtered and sorted names (question in register, records fixed)
  format     10 writing tasks with machine-checkable constraints (IFEval style)
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
items = []

def add(task, family, expected, plain, normal, ornate, check=None):
    items.append({"task": task, "family": family, "expected": expected, "check": check or {},
                  "variants": {"plain": plain, "normal": normal, "ornate": ornate}})

# ---------------------------------------------------------------- math
M = [
 ("m01", 30,
  "A bakery makes 240 cookies. It sells 3/4 of them in the morning. In the afternoon it sells half of the cookies that are left. How many cookies are left at the end of the day? Give only the number.",
  "A bakery bakes 240 cookies. It sells three quarters of them in the morning and half of the remaining cookies in the afternoon. How many cookies are left at the end of the day? Answer with the number only.",
  "A bakery produces a batch of 240 cookies, of which three quarters are disposed of through sales during the morning hours; during the afternoon, precisely half of the residual quantity is likewise sold. What number of cookies remains unsold upon the close of the day? Furnish solely the numerical figure, without accompanying exposition."),
 ("m02", 1300,
  "Maria gets $18 for each hour she works. She works 7 hours a day, 5 days a week. Each week she pays $210 for rent and $95 for food. How much money does she have left after 4 weeks? Give only the number.",
  "Maria earns $18 per hour. She works 7 hours a day, 5 days a week. Every week she spends $210 on rent and $95 on food. How much money does she have left after 4 weeks? Answer with the number only.",
  "Maria is remunerated at an hourly rate of $18 and discharges her duties for 7 hours per day across 5 days in each week. Her weekly outlays comprise $210 in rent and $95 in alimentary provisions. What residual sum remains at her disposal upon the conclusion of a 4-week interval? Furnish solely the numerical figure, without accompanying exposition."),
 ("m03", 190,
  "A train leaves at 9:40 and gets there at 13:15. A second train on the same route takes 25 minutes less. How many minutes does the second train take? Give only the number.",
  "A train departs at 9:40 and arrives at 13:15. A second train on the same route is 25 minutes faster. How many minutes does the second train's trip take? Answer with the number only.",
  "A train embarks upon its journey at 9:40 and attains its destination at 13:15. A second service traversing the identical route accomplishes the journey in 25 fewer minutes. What is the duration, expressed in minutes, of the second service's journey? Furnish solely the numerical figure, without accompanying exposition."),
 ("m04", 12,
  "A tank can hold 1,200 liters. Right now it is 40% full. A pump puts in 60 liters each minute. How many minutes until the tank is full? Give only the number.",
  "A tank holds 1,200 liters and is currently 40% full. A pump adds 60 liters per minute. How many minutes will it take to fill the tank? Answer with the number only.",
  "A reservoir possessing a total capacity of 1,200 liters is at present filled to 40% of said capacity. A pump introduces water at a rate of 60 liters per minute. How many minutes shall elapse before the reservoir attains complete fullness? Furnish solely the numerical figure, without accompanying exposition."),
 ("m05", 5,
  "A school has 4 classes with 28 kids in each. It also has 3 classes with 31 kids in each. One bus can take 45 kids. How many buses does the school need to take all the kids on a trip? Give only the number.",
  "A school has 4 classes of 28 students and 3 classes of 31 students. Each bus holds 45 students. How many buses are needed to take all the students on a trip? Answer with the number only.",
  "An educational institution comprises 4 classes of 28 pupils apiece together with 3 classes of 31 pupils apiece. Each available omnibus accommodates 45 pupils. How many omnibuses are requisite to convey the entire student body on an excursion? Furnish solely the numerical figure, without accompanying exposition."),
 ("m06", 50,
  "A jacket costs $80. The shop takes 25% off the price. Then Ana uses a coupon that takes $10 off the new price. How much does Ana pay? Give only the number.",
  "A jacket costs $80. It is on sale for 25% off, and Ana also has a coupon for $10 off the sale price. What is the final price Ana pays? Answer with the number only.",
  "A jacket bears a list price of $80. It is presently subject to a promotional reduction of 25%, and Ana additionally avails herself of a coupon conferring a further $10 deduction from the reduced price. What final sum does Ana remit? Furnish solely the numerical figure, without accompanying exposition."),
 ("m07", 36,
  "Sam is 3 times as old as his son. In 12 years, Sam will be 2 times as old as his son. How old is Sam now? Give only the number.",
  "Sam is three times as old as his son. In 12 years, Sam will be twice as old as his son. How old is Sam now? Answer with the number only.",
  "Sam's age is at present threefold that of his son. Upon the passage of 12 years, Sam's age shall be precisely double that of his son. What is Sam's present age? Furnish solely the numerical figure, without accompanying exposition."),
 ("m08", 300,
  "A farmer has 15 rows of apple trees. Each row has 12 trees. Each tree gives 40 apples. He puts the apples in boxes. Each box holds 24 apples. How many full boxes does he get? Give only the number.",
  "A farmer has 15 rows of apple trees with 12 trees in each row. Each tree produces 40 apples, and he packs the apples into boxes of 24. How many full boxes does he get? Answer with the number only.",
  "An agriculturalist cultivates 15 rows of apple trees, each row comprising 12 trees, and every tree yields 40 apples. The harvest is subsequently packed into containers accommodating 24 apples apiece. How many completely filled containers does he obtain? Furnish solely the numerical figure, without accompanying exposition."),
 ("m09", 49,
  "Lena's phone plan costs $25 each month. The first 100 texts are free. Each text after that costs $0.10. In March, Lena sent 340 texts. How many dollars was her bill for March? Give only the number.",
  "A phone plan costs $25 per month and includes 100 texts. Each text beyond the first 100 costs $0.10. Lena sent 340 texts in March. What was her bill for March in dollars? Answer with the number only.",
  "A mobile telephony subscription entails a monthly fee of $25 inclusive of an allowance of 100 text messages, with each message in excess of said allowance incurring a supplementary charge of $0.10. In the month of March, Lena dispatched 340 text messages. What was the total amount, in dollars, of her March invoice? Furnish solely the numerical figure, without accompanying exposition."),
 ("m10", 36.8,
  "Three friends eat out. The bill is $96. They add a 15% tip to the bill. Then they split the total in three equal parts. How many dollars does each friend pay? Give only the number.",
  "Three friends share a restaurant bill of $96. They add a 15% tip and split the total equally. How much does each friend pay in dollars? Answer with the number only.",
  "Three companions incur a restaurant bill amounting to $96. They supplement this sum with a gratuity of 15% and apportion the resulting total in equal shares among themselves. What amount, in dollars, is each companion obliged to contribute? Furnish solely the numerical figure, without accompanying exposition."),
]
for t, exp, p, n, o in M:
    add(t, "math", str(exp), p, n, o, {"type": "number"})

# ---------------------------------------------------------------- extract
EX_PLAIN = ("Read the order note below. Find five facts: the name of the customer, the product, how many they want, "
            "the day it must arrive, and the total price in euros. If the note changes a fact, use the new one. "
            "Give the answer as JSON with these keys: customer, product, quantity, delivery_date, total_eur. "
            "Write the date like 2026-03-14. Write quantity and total_eur as numbers. "
            "Write only the JSON. Do not write anything else.\n\nOrder note:\n{d}")
EX_NORMAL = ("Extract the following fields from the order note below: customer name, product, quantity, delivery date, "
             "and total price in euros. If the note corrects a value, use the corrected one. Return a JSON object with "
             "the keys customer, product, quantity, delivery_date, total_eur. Use YYYY-MM-DD for the date and plain "
             "numbers for quantity and total_eur. Return only the JSON.\n\nOrder note:\n{d}")
EX_ORNATE = ("Kindly undertake a meticulous examination of the order correspondence reproduced hereunder and distill "
             "therefrom the following salient particulars: the appellation of the commissioning customer, the "
             "merchandise in question, the requisite quantity, the stipulated date of delivery, and the aggregate "
             "consideration denominated in euros. Wherever the correspondence subsequently amends a previously "
             "articulated particular, the amended articulation shall be deemed authoritative. Render your findings as "
             "a JSON object whose keys are precisely customer, product, quantity, delivery_date, and total_eur, with "
             "the date expressed as YYYY-MM-DD and both quantity and total_eur expressed as unadorned numerals. Your "
             "response ought to comprise the JSON object exclusively, devoid of any prefatory or concluding "
             "commentary.\n\nOrder correspondence:\n{d}")
EX = [
 ("e01", "Hi, this is Laura Becker from Becker Design. We'd like 12 desk lamps delivered on March 3, 2026. "
         "The quote you sent says 540 euros in total, which works for us.",
  {"customer": "Laura Becker", "product": "desk lamp", "quantity": 12, "delivery_date": "2026-03-03", "total_eur": 540}),
 ("e02", "Order from Tomas Novak: 4 office chairs, total 1,196 EUR, needed by 2026-05-20. "
         "Update from Tomas an hour later: please make it 5 chairs, new total 1,495 EUR, same date.",
  {"customer": "Tomas Novak", "product": "office chair", "quantity": 5, "delivery_date": "2026-05-20", "total_eur": 1495}),
 ("e03", "Good morning! Priya Shah here. I ordered 30 coffee mugs last week for delivery on 10 April 2026, total 180 euros. "
         "Sorry, the event moved, so please deliver them on 14 April 2026 instead. Everything else stays the same.",
  {"customer": "Priya Shah", "product": "coffee mug", "quantity": 30, "delivery_date": "2026-04-14", "total_eur": 180}),
 ("e04", "From: Marco Rossi. I need 2 standing desks. My colleague Anna Weber will sign for them. "
         "Please deliver on June 2, 2026. Your invoice says €1,380.00 total.",
  {"customer": "Marco Rossi", "product": "standing desk", "quantity": 2, "delivery_date": "2026-06-02", "total_eur": 1380}),
 ("e05", "Hello, Sofia Lind. Last year we bought 50 notebooks from you. This time we want 80 notebooks, "
         "delivered on 2026-09-01. Total price as quoted: 240 euros.",
  {"customer": "Sofia Lind", "product": "notebook", "quantity": 80, "delivery_date": "2026-09-01", "total_eur": 240}),
 ("e06", "Kenji Watanabe here. Please send 6 monitor arms. Price is 45 euros each, so 270 euros total. "
         "Delivery on November 18, 2026, not November 8 as I wrote in my first email.",
  {"customer": "Kenji Watanabe", "product": "monitor arm", "quantity": 6, "delivery_date": "2026-11-18", "total_eur": 270}),
 ("e07", "This is Olga Petrova. We'd like 3 whiteboards. Delivery: 2026-02-27. Total: 375 EUR. "
         "P.S. we might order 10 more next quarter, but not now.",
  {"customer": "Olga Petrova", "product": "whiteboard", "quantity": 3, "delivery_date": "2026-02-27", "total_eur": 375}),
 ("e08", "Hi team, David Cohen. Order: 25 USB cables, delivery July 7, 2026, total 125 euros. "
         "Correction: we only need 20 cables, so the total is 100 euros.",
  {"customer": "David Cohen", "product": "USB cable", "quantity": 20, "delivery_date": "2026-07-07", "total_eur": 100}),
 ("e09", "Hello, I am writing for my manager, Elena Garcia, who is placing this order. She needs 8 ergonomic keyboards "
         "delivered on 2026-10-05. The total is 720 euros. You can reply to me, Paul.",
  {"customer": "Elena Garcia", "product": "ergonomic keyboard", "quantity": 8, "delivery_date": "2026-10-05", "total_eur": 720}),
 ("e10", "Ahmed Karim here. Please deliver 15 filing cabinets on December 1, 2026. Total 2,250 euros. "
         "Our old cabinets cost 120 euros each in 2019, so this price is fine.",
  {"customer": "Ahmed Karim", "product": "filing cabinet", "quantity": 15, "delivery_date": "2026-12-01", "total_eur": 2250}),
]
for t, d, exp in EX:
    add(t, "extract", json.dumps(exp), EX_PLAIN.format(d=d), EX_NORMAL.format(d=d), EX_ORNATE.format(d=d),
        {"type": "json_fields", "fields": exp})

# ---------------------------------------------------------------- classify
CL_PLAIN = ("Read the message from a customer below. Pick one group for it:\n"
            "- billing: money, bills, charges, or payments\n"
            "- shipping: getting the package, delivery, or tracking\n"
            "- account: logging in, passwords, or account settings\n"
            "- technical: the app or website does not work right, errors, or crashes\n"
            "If the message talks about more than one thing, pick the group of the main problem the customer wants fixed. "
            "Write only the group name.\n\nMessage:\n{d}")
CL_NORMAL = ("Classify the customer message below into exactly one category:\n"
             "- billing: charges, invoices, payments\n"
             "- shipping: delivery, tracking, lost packages\n"
             "- account: login, passwords, account settings\n"
             "- technical: app or website errors, bugs, crashes\n"
             "If the message mentions several topics, choose the category of the main problem the customer wants "
             "resolved. Reply with the category name only.\n\nMessage:\n{d}")
CL_ORNATE = ("Your task entails the assignment of the customer communication reproduced below to precisely one of the "
             "following taxonomic categories:\n"
             "- billing: matters pertaining to charges, invoicing, or the remittance of payment\n"
             "- shipping: matters pertaining to the conveyance, tracking, or misplacement of consignments\n"
             "- account: matters pertaining to authentication, credentials, or the configuration of user accounts\n"
             "- technical: matters pertaining to malfunctions, defects, or anomalous behaviour of the application or website\n"
             "Should the communication allude to a multiplicity of topics, the determinative consideration shall be the "
             "principal grievance for which the customer seeks redress. Your reply should consist of the category "
             "designation alone, unaccompanied by any elaboration.\n\nCommunication:\n{d}")
CL = [
 ("k01", "shipping", "My payment went through fine and I got the receipt, thanks. But the tracking page has not changed in 6 days and the parcel still hasn't arrived. Where is it?"),
 ("k02", "billing", "I see two charges of 49.99 on my card for the same order. I only placed one order. Please refund the extra one."),
 ("k03", "account", "I changed my phone and now the login code goes to my old number. I can't get into my account. The app itself works fine."),
 ("k04", "technical", "Every time I tap 'Export to PDF' the app closes. I reinstalled it twice. My subscription is paid and active."),
 ("k05", "billing", "The package arrived on time, great. But the invoice shows 3 items and I only ordered 2. I want the invoice corrected and the extra amount returned."),
 ("k06", "account", "How do I change the email address on my profile? I no longer use the old one."),
 ("k07", "shipping", "Your courier left my box at the wrong address, number 14 instead of 41. The neighbor says they never got it."),
 ("k08", "technical", "The checkout page shows an error 500 when I click Pay, so I can't finish my order. I tried two browsers."),
 ("k09", "account", "Someone else's name shows up in my account settings and I did not change it. I want my own details back and my password reset."),
 ("k10", "billing", "I cancelled my plan in May but you charged me again in June and July. The app and delivery are fine, I just want my money back for those months."),
]
for t, lab, d in CL:
    add(t, "classify", lab, CL_PLAIN.format(d=d), CL_NORMAL.format(d=d), CL_ORNATE.format(d=d),
        {"type": "label", "labels": ["billing", "shipping", "account", "technical"]})

# ---------------------------------------------------------------- filter
F = [
 ("f01", "Anna, David, Greta",
  "Anna - Berlin - 34\nBen - Munich - 41\nClara - Berlin - 30\nDavid - Berlin - 52\nEva - Hamburg - 29\nFelix - Berlin - 27\nGreta - Berlin - 31",
  "Here is a list of workers. Each line has a name, a city, and an age.\n{d}\nWhich workers live in Berlin and are more than 30 years old? Put the names in A to Z order. Write only the names, with commas between them.",
  "Below is a list of employees with their city and age.\n{d}\nList the employees who live in Berlin and are older than 30, in alphabetical order. Reply with the names only, comma separated.",
  "Presented hereunder is a roster of personnel, each entry delineating the individual's name, municipality of residence, and age.\n{d}\nEnumerate those personnel who are domiciled in Berlin and whose age surpasses thirty years, arranged in ascending alphabetical sequence. Your response should comprise solely their names, delimited by commas."),
 ("f02", "Notebook, Lamp, Pillow",
  "Lamp - 18 euros - in stock\nMug - 8 euros - out of stock\nNotebook - 5 euros - in stock\nKettle - 25 euros - in stock\nPillow - 19 euros - in stock\nCandle - 12 euros - out of stock\nClock - 20 euros - in stock",
  "Here is a list of things a shop sells, with the price and if the shop has them now.\n{d}\nWhich things cost less than 20 euros and are in stock? Start with the cheapest one and end with the most costly one. Write only the names, with commas between them.",
  "Below is a product list with prices and stock status.\n{d}\nList the products that cost under 20 euros and are in stock, sorted from cheapest to most expensive. Reply with the names only, comma separated.",
  "The following inventory delineates each article's price and its present availability.\n{d}\nIdentify those articles whose price falls below 20 euros and which are presently available in stock, ordered from the least to the most costly. Your response should comprise solely their names, delimited by commas."),
 ("f03", "T-3, T-4, T-6",
  "T-1 - open - Lee\nT-2 - done - Kim\nT-3 - open - Kim\nT-4 - in progress - Ravi\nT-5 - done - Lee\nT-6 - open - Ravi\nT-7 - in progress - Lee",
  "Here is a list of tasks. Each line has the task ID, its status, and the person who owns it.\n{d}\nWhich tasks are not done and are not owned by Lee? Keep them in the same order as the list. Write only the task IDs, with commas between them.",
  "Below is a task list with status and owner.\n{d}\nList the tasks that are not done and not owned by Lee, in the order they appear. Reply with the task IDs only, comma separated.",
  "Presented hereunder is a register of tasks, each entry specifying its identifier, its present status, and its designated owner.\n{d}\nEnumerate those tasks which have not attained completion and whose ownership does not reside with Lee, preserving the sequence in which they appear. Your response should comprise solely their identifiers, delimited by commas."),
 ("f04", "Cem, Fay, Bea, Emil",
  "Ali - math 88 - science 65\nBea - math 72 - science 70\nCem - math 95 - science 81\nDana - math 69 - science 90\nEmil - math 70 - science 77\nFay - math 81 - science 74",
  "Here are test scores for some students.\n{d}\nWhich students got 70 or more in math and also 70 or more in science? Start with the highest math score and go down. Write only the names, with commas between them.",
  "Below are students' test scores.\n{d}\nList the students who scored at least 70 in both math and science, sorted by math score from highest to lowest. Reply with the names only, comma separated.",
  "The following tabulation records the examination results attained by a cohort of students.\n{d}\nIdentify those students whose scores attained or exceeded 70 in mathematics and, concurrently, in science, ordered by descending mathematics score. Your response should comprise solely their names, delimited by commas."),
 ("f05", "Marseille, Lyon, Toulouse",
  "Lyon - 520000\nParis (capital) - 2100000\nMarseille - 870000\nNice - 340000\nToulouse - 500000\nBern (capital) - 140000\nZurich - 420000",
  "Here is a list of cities and how many people live in each.\n{d}\nFind the 3 biggest cities that are not capitals. Start with the biggest. Write only the city names, with commas between them.",
  "Below is a list of cities with their populations.\n{d}\nList the three largest cities that are not capitals, largest first. Reply with the city names only, comma separated.",
  "The following compilation enumerates a number of municipalities alongside their respective populations.\n{d}\nIdentify the three most populous municipalities that do not hold the status of a capital, arranged in descending order of population. Your response should comprise solely their names, delimited by commas."),
 ("f06", "AZ102, AZ103, FR300",
  "AZ101 - 09:55 - Rome\nAZ102 - 10:00 - Milan\nLH200 - 11:30 - Munich\nAZ103 - 12:15 - Rome\nFR300 - 14:00 - Milan\nAZ104 - 14:05 - Rome\nU2400 - 13:20 - Naples",
  "Here is a list of flights. Each line has the flight code, the time it leaves, and where it goes.\n{d}\nWhich flights go to Rome or Milan and leave from 10:00 to 14:00? Count 10:00 and 14:00 too. Put them in time order. Write only the flight codes, with commas between them.",
  "Below is a list of departures with flight code, time, and destination.\n{d}\nList the flights to Rome or Milan that depart between 10:00 and 14:00 inclusive, in order of departure time. Reply with the flight codes only, comma separated.",
  "Presented hereunder is a schedule of departures, each entry specifying the flight designation, the time of departure, and the destination.\n{d}\nEnumerate those flights bound for either Rome or Milan whose departure falls within the interval from 10:00 to 14:00, both endpoints inclusive, arranged in chronological order of departure. Your response should comprise solely their designations, delimited by commas."),
 ("f07", "Dune, Contact, Hyperion, Snow Crash",
  "Dune - 1965 - 412 pages\nNeuromancer - 1984 - 271 pages\nHyperion - 1989 - 482 pages\nSnow Crash - 1992 - 480 pages\nThe Road - 2006 - 287 pages\nAnathem - 2008 - 937 pages\nContact - 1985 - 432 pages",
  "Here is a list of books, with the year each came out and how many pages it has.\n{d}\nWhich books came out before 2000 and have more than 300 pages? Start with the oldest book. Write only the titles, with commas between them.",
  "Below is a list of books with publication year and page count.\n{d}\nList the books published before 2000 that have more than 300 pages, oldest first. Reply with the titles only, comma separated.",
  "The following bibliography records, for each volume, its year of publication and its length in pages.\n{d}\nIdentify those volumes published prior to the year 2000 whose length exceeds 300 pages, arranged in chronological order of publication commencing with the earliest. Your response should comprise solely their titles, delimited by commas."),
 ("f08", "web-1, db-1, api-1, api-2",
  "web-1 - eu-west - CPU 85% - up\nweb-2 - us-east - CPU 92% - up\ndb-1 - eu-west - CPU 40% - down\ndb-2 - us-east - CPU 30% - up\ncache-1 - eu-west - CPU 80% - up\napi-1 - eu-west - CPU 91% - up\napi-2 - us-east - CPU 10% - down",
  "Here is a list of servers. Each line has the name, the region, the CPU use, and if it is up or down.\n{d}\nPick two kinds of servers: servers in eu-west with CPU above 80%, and any server in any region that is down. Keep them in the same order as the list. Write only the server names, with commas between them.",
  "Below is a list of servers with region, CPU usage, and status.\n{d}\nList the servers that are in eu-west with CPU above 80%, plus any server, in any region, whose status is down, in the order they appear. Reply with the server names only, comma separated.",
  "Presented hereunder is an inventory of servers, each entry specifying its designation, region, processor utilisation, and operational status.\n{d}\nEnumerate those servers which either reside in eu-west with processor utilisation in excess of 80%, or whose operational status is down irrespective of region, preserving the sequence in which they appear. Your response should comprise solely their designations, delimited by commas."),
 ("f09", "banana, lemon, lime, plum",
  "apple - red - 2 euros per kg\nbanana - yellow - 1 euro per kg\ncherry - red - 6 euros per kg\nkiwi - green - 4 euros per kg\nlemon - yellow - 2 euros per kg\nlime - green - 1 euro per kg\nplum - purple - 3 euros per kg\ngrape - green - 5 euros per kg",
  "Here is a list of fruits, with the color and the price.\n{d}\nWrite all the fruits, but leave out the red ones. Also leave out the ones that cost more than 3 euros per kg. Put the names in A to Z order. Write only the names, with commas between them.",
  "Below is a list of fruits with color and price.\n{d}\nList all the fruits except those that are red or cost more than 3 euros per kg, in alphabetical order. Reply with the names only, comma separated.",
  "The following catalogue records, for each fruit, its colour and its price per kilogram.\n{d}\nEnumerate every fruit with the exception of those exhibiting a red colouration or commanding a price in excess of 3 euros per kilogram, arranged in ascending alphabetical sequence. Your response should comprise solely their names, delimited by commas."),
 ("f10", "INV-15, INV-11, INV-14",
  "INV-11 - unpaid - 45 days old - 300 euros\nINV-12 - paid - 60 days old - 900 euros\nINV-13 - unpaid - 30 days old - 700 euros\nINV-14 - unpaid - 31 days old - 150 euros\nINV-15 - unpaid - 90 days old - 1200 euros\nINV-16 - paid - 10 days old - 50 euros\nINV-17 - unpaid - 12 days old - 400 euros",
  "Here is a list of bills. Each line has the bill number, if it is paid, how old it is, and the amount.\n{d}\nWhich bills are not paid and are more than 30 days old? Start with the biggest amount and end with the smallest. Write only the bill numbers, with commas between them.",
  "Below is a list of invoices with payment status, age, and amount.\n{d}\nList the invoices that are unpaid and more than 30 days old, sorted from the largest amount to the smallest. Reply with the invoice numbers only, comma separated.",
  "Presented hereunder is a ledger of invoices, each entry specifying its number, settlement status, age, and amount.\n{d}\nEnumerate those invoices which remain unsettled and whose age exceeds 30 days, arranged in descending order of amount. Your response should comprise solely their numbers, delimited by commas."),
]
for t, exp, d, p, n, o in F:
    add(t, "filter", exp, p.format(d=d), n.format(d=d), o.format(d=d), {"type": "list"})

# ---------------------------------------------------------------- format (constraint following)
CAPITALS = ["amsterdam", "andorra la vella", "athens", "belgrade", "berlin", "bern", "bratislava", "brussels",
            "bucharest", "budapest", "chisinau", "copenhagen", "dublin", "helsinki", "kyiv", "kiev", "lisbon",
            "ljubljana", "london", "luxembourg", "madrid", "minsk", "monaco", "moscow", "oslo", "paris",
            "podgorica", "prague", "reykjavik", "riga", "rome", "san marino", "sarajevo", "skopje", "sofia",
            "stockholm", "tallinn", "tirana", "vaduz", "valletta", "vatican city", "vienna", "vilnius",
            "warsaw", "zagreb", "pristina", "nicosia", "tbilisi", "yerevan", "baku", "ankara"]
FMT = [
 ("c01", {"type": "bullets", "n": 3, "forbid": ["health"]},
  "Write 3 points about why sleep is good for you. Start each point with a dash and a space (\"- \"). Do not use the word \"health\". Write only the 3 points.",
  "Write exactly 3 bullet points on why sleep matters. Start each bullet with \"- \". Do not use the word \"health\". Output only the bullets.",
  "Compose precisely three bullet points elucidating the significance of sleep, each commencing with a hyphen followed by a single space (\"- \"). The lexeme \"health\" must be scrupulously avoided. Your output should consist of the three bullet points exclusively."),
 ("c02", {"type": "one_sentence", "max_words": 14, "end": "!"},
  "Write one sentence about the ocean. Use fewer than 15 words. End the sentence with \"!\". Write only that sentence.",
  "Write a single sentence about the ocean in fewer than 15 words, ending with an exclamation mark. Output only the sentence.",
  "Compose a solitary sentence pertaining to the ocean, comprising fewer than fifteen words and terminating in an exclamation mark. Your output should consist of that sentence exclusively."),
 ("c03", {"type": "upper_lines", "n": 5, "allowed": CAPITALS},
  "Name 5 capital cities in Europe. Put each one on its own line. Use only CAPITAL LETTERS. Do not put numbers or dashes in front. Write nothing else.",
  "List 5 European capital cities, one per line, written in all capital letters, with no numbering or bullets. Output nothing else.",
  "Enumerate five capital cities situated within Europe, each occupying a discrete line and rendered entirely in uppercase characters, without any numbering, bullets, or other prefatory marks. Refrain from producing any additional content."),
 ("c04", {"type": "paragraphs", "n": 2, "require": ["steel"], "forbid": ["plastic"]},
  "Write a short text to sell a water bottle. Write exactly 2 paragraphs. Put an empty line between them. Use the word \"steel\". Do not use the word \"plastic\". Write only the 2 paragraphs.",
  "Write a short product description for a water bottle in exactly 2 paragraphs separated by a blank line. Include the word \"steel\" and do not use the word \"plastic\". Output only the description.",
  "Compose a concise promotional description of a water bottle structured as precisely two paragraphs demarcated by a single blank line. The term \"steel\" must be incorporated, whereas the term \"plastic\" must be entirely eschewed. Your output should consist of the description exclusively."),
 ("c05", {"type": "lines_start", "n": 3, "letter": "s"},
  "Write a short poem about autumn. It must have exactly 3 lines. Each line must start with the letter \"S\". Write only the poem.",
  "Write a three-line poem about autumn in which every line begins with the letter \"S\". Output only the poem.",
  "Compose a poem of precisely three lines on the theme of autumn, wherein each line commences with the letter \"S\". Your output should consist of the poem exclusively."),
 ("c06", {"type": "title", "max_words": 6, "forbid_chars": ":"},
  "Write a title for a blog post about saving money. Every word must start with a capital letter. Use 6 words or fewer. Do not use a colon. Write only the title.",
  "Write a title for a blog post about saving money. Capitalize the first letter of every word, use at most 6 words, and do not use a colon. Output only the title.",
  "Devise a title for a blog article concerning the accumulation of savings, wherein the initial letter of every constituent word is capitalised, the total word count does not exceed six, and no colon is employed. Your output should consist of the title exclusively."),
 ("c07", {"type": "json_fields", "fields": {"city": "Paris", "country": "France"}},
  "In what city and country is the Eiffel Tower? Answer as JSON with two keys: \"city\" and \"country\". Write only the JSON.",
  "Where is the Eiffel Tower? Reply with a JSON object with the keys \"city\" and \"country\", and nothing else.",
  "Ascertain the geographical location of the Eiffel Tower and articulate it as a JSON object bearing precisely the keys \"city\" and \"country\". Your response should comprise the JSON object exclusively."),
 ("c08", {"type": "rhymes", "n": 4, "suffix": "at", "exclude": "cat"},
  "Give 4 words that rhyme with \"cat\". Do not use \"cat\" itself. Write them in small letters. Put commas between them. Write nothing else.",
  "List 4 words that rhyme with \"cat\" (not \"cat\" itself), in lowercase, separated by commas. Output nothing else.",
  "Enumerate four lexical items that rhyme with \"cat\", excluding \"cat\" itself, rendered in lowercase characters and delimited by commas. Refrain from producing any additional content."),
 ("c09", {"type": "two_sentences_q", "word": "friday", "count": 1},
  "Write a reminder about a team meeting on Friday at 3 pm. Use exactly 2 sentences. The first sentence must be a question. Use the word \"Friday\" only one time. Write only the reminder.",
  "Write a two-sentence reminder about a team meeting on Friday at 3 pm. The first sentence must be a question, and the word \"Friday\" must appear exactly once. Output only the reminder.",
  "Compose a reminder, comprising precisely two sentences, concerning a team meeting scheduled for Friday at 3 pm. The initial sentence must take the form of an interrogative, and the word \"Friday\" must occur on exactly one occasion. Your output should consist of the reminder exclusively."),
 ("c10", {"type": "repeat", "word": "yes", "n": 7},
  "Write the word \"yes\" 7 times. Put one space between each one. Write nothing else.",
  "Repeat the word \"yes\" exactly 7 times, separated by single spaces. Output nothing else.",
  "Reproduce the word \"yes\" on precisely seven occasions, each instance separated from the next by a single space. Refrain from producing any additional content."),
]
for t, chk, p, n, o in FMT:
    add(t, "format", "", p, n, o, chk)

assert len(items) == 50, len(items)
assert len({i["task"] for i in items}) == 50
(HERE / "prompts.json").write_text(json.dumps(items, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"wrote {len(items)} tasks x 3 registers -> prompts.json")
