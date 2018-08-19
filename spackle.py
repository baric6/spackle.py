###############################################################################
# This first part of the program receives the web-page by a html-get request
# then saves the url in whatever var u want in python console
# ex.. html = *main function name*(url), from there you can do as you please
# scroll down for examples
# this program is a generic html getter meaning can be used with all valid
# html, instead of being hard coded, very nice :}
###############################################################################
#
# Notes by Baric
# taken from "https://realpython.com/python-web-scraping-practical-introduction/" as learning reference :}


from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


# main function for first part getting page.html
def get_the_page(url):
    try:
        # gets content of page using a http get request
        # if page not found gives a error
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error('Error during request to {0} : 1'.format(url, str(e)))
        return None


# for if statement in main function, to see id connection is good
def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    # comparing using the == not =
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


# for the requestException to print log error 'error during request'
def log_error(e):
    print(e)

###############################################################################
# to run part below use fallowing code in python console
#
# ***from file :: gets my python file Then imports my function***
# from spackle import get_the_page
#
# ***saves the html in raw_data :: make sure to make url a string using '' ***
# raw_html = get_the_page('https://en.wikipedia.org/wiki/Cat_Fancy')
#
# ***len(arg) tells me how long my web page is if 0 then no page was loaded***
# len(raw_html)
#
# ***saves the web page in no_html if any***
# no_html = get_the_page('https://en.wikipedia.org/wiki/Cat_Fancy')
#
# ***if true there is not a web-page stored in no html***
# ***if false there is a page stored in no_html***
# ***note***
# ***maybe should do this before hand to check if site is a real site or not***
# ***then parse the site to see the length***
# no_html is None
#
#
###############################################################################
#                                                                             #
#              using beautiful soup to print data in a loop                   #
#                                                                             #
###############################################################################
# ***in py console type this with BeautifulSoup***
# ***this part will print doubles if there are doubles in html source, will refine later***
#
# ***raw_html is where the html source code is stored***


# raw_html = get_the_page("http://www.fabpedigree.com/james/mathmen.htm")
#
# ***using html = beautifulSoup with the source code and parser to gather the data needed***
# ***the line below sets the source code of raw_html and selected parser to html, the parser turns the raw_html to***
# ***a txt file formatted in html***
# html = BeautifulSoup(raw_html, "html.parser")
#
# ***having a for-loop loop threw each piece line of data saving it in 'html_li = (can name it whatever)' then print**
# ***html_li is in <li> tag where the names are stored on the web page***
# ***out each line, kinda like Getline() in a loop like in c++ with a file, but the file is a web-page***
# ***the html.select(*<add tag you would like to search threw html>*)***, searches the
# ***html to print what in the html tag marker that you selected***
# for i, html_li in enumerate(html.select("li")):
#    print(i, html_li.text)

###############################################################################
#                                                                             #
#              Function that makes sure there are no double names             #
#                                                                             #
###############################################################################

def get_name():
    # The web address that is save as a string into url
    url = 'http://www.fabpedigree.com/james/mathmen.htm'
    # passing the url to the first function, that connects to a web-page or errors out
    response = get_the_page(url)

    # its saying if you have a response from site do this, else raise a exception 'not-found'
    if response is not None:
        # passes the html source code to parser then saves a txt formatted like html in html
        html = BeautifulSoup(response, "html.parser")
        # a unordered set of names that is: iterable(able to move threw), mutable(able to change values)
        # and have no duplicates in a listing of data
        names = set()
        # a for-loop that sets 'html_line = 0', then like in c++ 'html_line < li' :: li = the number of <li> tags
        # in the html file
        # so if '<li>' = 'amount_of_names' then in c++, 'for(html = 0; html < amount_of_names; html++)';
        for html_line in html.select("li"):
            # splits the string from a solid line by the \n at the end of each name and stacks the names
            # so if there are 20 '\n(or new lines)', then in c++, 'for(name = 0; name < 20; name++)';
            for name in html_line.text.split("\n"):
                # if split string length is not null/0, if is zero raise exception 'error'
                if len(name) > 0:
                    # the .strip function strips the data before and after the string including white space
                    # it stripes it because it is taken out of a html file and this cleans it up
                    # the .add adds the striped string to the names set(line 115)
                    names.add(name.strip())
        # lets you pass the names in a list style, that above just processed, so you can call it out of
        # functions scope, like a function in c++
        return list(names)
    # if something fails up above this exception gets thrown
    raise Exception("Error retrieving contents at {}".format(url))

###############################################################################
#                                                                             #
#             Function to get how many web-views of a mathematicians          #
#                                                                             #
###############################################################################


# defined a function that gets passed the value from above function
def get_hits_on_name(names):
    # the web-site that has click stats in asumming i need to make a login but on the to do
    # but takes me to mediaWiki/metWiki
    url_root = 'https://xtools.wmflabs.org/articleinfo/en.wikipedia.org/{}'
    # passing the wiki page to my first function to see if it will connect/respond
    response = get_the_page(url_root.format(name))

    # if the site responds then next, or it will throw a error
    if response is not None:
        # the html is passed to a parser that generates a .txt of the html that is formatted like html, then
        # saved in html as a txt
        html = BeautifulSoup(response, "html.parser")
        # hit_link looks for the <a>(anchor for href), then goes to the 'href' in the <a>, and the uncommon
        # words in "<a> href " is latest-60 is the uncommon substring so it looks there
        # uses a for loop to loop threw all '<a> href latest-60'
        hit_link = [a for a in html.select("a")
                    if a["href"].find("latest-60") > -1]
        # strip commas
        # if hit_link > 0 then replace the commas with spaces
        if len(hit_link) > 0:
            link_text = hit_link[0].text.replace(",", "")

            # convert to int
            # the link test is a string when saved from hit_link[0].text.replace when returns int will
            # convert the number string into int
            # if no number is stored link_text then will error out 'cant turn into a int'
        try:
            return int(link_text)

        except:
            log_error("could not parse {} as an 'int' ".format(link_text))
    # if no response will do log_error
    log_error("No pageviews found for {}".format(name))
    return None

###############################################################################
#                                                                             #
#       The main function that calls all of the previous functions            #
#                                                                             #
###############################################################################


# if imported to another program this part of the program will not run, by using the
# __name__ == "__main__" function it will only run when spackle.py is run not imported,
# if imported it will run all the code above witch is useful to be able to port depending on
# what i an trying to do :}
if __name__ == "__main__":
    print("Getting the list of names.....")
    # calling 'get_name' function to start getting name from site and sets the array/list to names
    names = get_name()
    print(".....done")

    # makes results a array/list...weird syntax :/
    results = []

    print("Getting stats for each name.....")
    # for loop that goes as long as the amount of names entry
    for name in names:
        try:
            # calling 'get_hits_on_name' and sets the array/list to hits
            hits = get_hits_on_name(name)
            # None is not a value it is a place-holder for a variable that will be put in later
            # but if hits == None this far in the program the error message will display and halt the program
            # 'if hits == None' in other words... i like the operator == better :/
            if hits is None:
                hits -1
            # so if hits have no value/string append name to hits :: ex... albert 232353214 web-views
            results.append((hits, name))
            # if hits have a name but no value then skip till to the value that has both "name :: hits"
            # will keep skipping till it has only the ones with the "name :: hits"
        except:
            results.append((-1, name))
            log_error("Error encountered while processing '{}', Skipping".format(name))

    print("....done.\n")
    # this calls the sorting function to sort the results as a list, sorting them in acceding order
    # as-in [1, 2, 3]
    results.sort()
    # the results.reverse() takes the assorted list in acceding order and reverses it so that the bigger number
    # is now the top number as in [1, 2, 3] to [3, 2, 1], good for seeing the top scores of items
    results.reverse()
    # if there are more than five results, then show the top 5, save the five to top_marks
    if len(results) > 5:
        top_marks = results[0:5]
    # if there are less then 5 results in the list save them to top_marks
    else:
        top_marks = results
    # for-loop that loops as many times that there are varables in top_marks,
    # and print the mathematician and the marks to the screen, the if statement above will only loop a max of 5 or less
    # to change that make "if len(results) > 6", then change the results[0:6] and should display six results
    print("\nThe most popular mathematicians are:\n")
    for (mark, mathematicians) in top_marks:
        print("{} with {} page-views".format(mathematicians, mark))
    # if the list is
    no_results = len([res for res in results if res[0] == -1])
    print("\nBut we did not find the results for '{}' mathematicians on the list".format(no_results))