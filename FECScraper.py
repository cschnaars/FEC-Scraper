# FEC Scraper
# By Christopher Schnaars and Anthony DeBarros, USA TODAY
# Developed with Python 2.7.2

"""
The purpose of this script is to scrape campaign finance reports
from the Federal Election Commission (FEC) website for a specified
group of committees.

You are strongly encouraged to consult the documentation in README.txt
before using this scraper so you'll understand what it does (and does
not) do. In a nutshell, it captures only Form 3 filings by committees
you specify below.

Optionally, the script can interact with a database to help manage
your downloaded data. Complete details can be found in README.txt.
To do this, make sure the usedatabaseflag user variable is set to 1.

You can specify up to three directories for various files:
 * savedir: This is where scraped files will be saved.
 * reviewdir: This is a directory where you can house files that you have not
imported into your database because the data requires cleanup before it
can be successfully imported. This script uses this directory only to look
for files that previously have been downloaded. No files in this directory
will be altered, and no new files will be saved here.
 * processeddir: Similarly, you can put files you've already imported
into a database in this directory. As with reviewdir, the script will use
this directory only to look for files that previously have been downloaded.
It will not alter files in this directory or save new files here.

You'll find commented code below to show you how to explicitly
download filings for a particular committee.
"""

# User variables

# Try to import your user settings or set them explicitly. The database
# connection string will be ignored if database integration is disabled.
try:
    exec(open('usersettings.py').read())
except:
    maindir = 'C:\\data\\Python\\FEC\\'
    connstr = 'DRIVER={SQL Server};SERVER=;DATABASE=FEC;UID=;PWD=;'
    
# Directories: You can edit these to customize file locations.
savedir = maindir + 'Import\\'
reviewdir = maindir + 'Review\\'
processeddir = maindir + 'Processed\\'

# Set this flag to 1 if you want the script to interact with a database.
# Set it to 0 if the script should run independent of any database.
# A database is used solely to look for committees and files that
# previously have been downloaded.
usedatabaseflag = 0

# Import libraries
import re, urllib, glob, os

# Create lists to hold committee and file IDs
commidlist = []
fileidlist = []

# Create database connection to fetch lists of committee IDs and file IDs already in the database
# The code below works with SQL Server; see README for tips on connecting
# to other database managers.
if usedatabaseflag == 1:
    import pyodbc
    conn = pyodbc.connect(connstr)
    cursor = conn.cursor()
    sql = 'EXEC usp_GetCommitteeIDs'

    # Execute stored procedure and populate list with committee IDs
    sql = 'EXEC usp_GetCommitteeIDs'
    for row in cursor.execute(sql):
        commidlist += row

    # Execute stored procedure and populate list with file IDs
    sql = 'EXEC usp_GetFileIDs'
    for row in cursor.execute(sql):
        fileidlist += row

    # Close database connection
    conn.close()

# Add IDs for files in review directory
for datafile in glob.glob(os.path.join(reviewdir, '*.fec')):
    fileidlist.append(datafile.replace(reviewdir, '')[:6])

# Add IDs for files in save directory
for datafile in glob.glob(os.path.join(savedir, '*.fec')):
    fileidlist.append(datafile.replace(savedir, '')[:6])

# Sort the fileid list
fileidlist.sort()

# If you need to add committee IDs for candidates or PACs for which
# you've never previously downloaded data, you can do that here like this:
#commidlist.append('C00431445') # Obama for America
#commidlist.append('C00500587') # RickPerry.org Inc.
#commidlist.append('C00431171') # Romney for President Inc.
commidlist.append('C00500587') # RickPerry.org Inc.
commidlist.append('C00431171') # Romney for President Inc.
commidlist.append('C00496034') # Rick Santorum for President
commidlist.append('C00495820') # Ron Paul 2012 Presidential Campaign Committee Inc.
commidlist.append('C00431445') # Obama for America
commidlist.append('C00498444') # Jon Huntsman for President Inc.
commidlist.append('C00497511') # Bachmann for President
commidlist.append('C00496067') # Friends of Herman Cain Inc.
commidlist.append('C00496497') # Newt 2012
commidlist.append('C00494393') # Pawlenty for President
commidlist.append('C00495622') # Gary Johnson 2012 Inc.
commidlist.append('C00200584') # Upton for All of Us (Rep. Fred Upton, R-Mich., debt supercommittee)
commidlist.append('C00255562') # Friends of Jim Clyburn
commidlist.append('C00264101') # Becerra for Congress
commidlist.append('C00347476') # Dave Camp for Congress
commidlist.append('C00366096') # Van Hollen for Congress
commidlist.append('C00370650') # Friends of Jeb Hensarling
commidlist.append('C00413096') # Kansans for Huelskamp
commidlist.append('C00435628') # Allen West for Congress
commidlist.append('C00459461') # Friends of Dennis Ross
commidlist.append('C00460550') # Jeff Duncan for Congress
commidlist.append('C00463877') # Sandy Adams for Congress
commidlist.append('C00464602') # Vicky Hartzler for Congress
commidlist.append('C00466854') # Steve Fincher for Congress
commidlist.append('C00471292') # Mulvaney for Congress
commidlist.append('C00472712') # Landry for Louisiana
commidlist.append('C00472878') # Diane Black for Congress
commidlist.append('C00473132') # MCKINLEY FOR CONGRESS
commidlist.append('C00473579') # JOE WALSH FOR CONGRESS COMMITTEE, INC.
commidlist.append('C00473736') # ELECT BLAKE FARENTHOLD COMMITTEE
commidlist.append('C00477323') # PALAZZO FOR CONGRESS
commidlist.append('C00482281') # FRIENDS OF RICH NUGENT
commidlist.append('C00490003') # 2010 LEADERSHIP COUNCIL
commidlist.append('C00489641') # ACCOUNTABILITY 2010
commidlist.append('C00484287') # AFL-CIO WORKERS' VOICES PAC
commidlist.append('C00489385') # ALASKANS STANDING TOGETHER
commidlist.append('C00489708') # ALLIANCE TO PROTECT TAXPAYERS
commidlist.append('C00497081') # AMERICA FOR THE PEOPLE PAC
commidlist.append('C00494278') # AMERICA GET UP
commidlist.append('C00492520') # AMERICA VOTES ACTION FUND
commidlist.append('C00487744') # AMERICA'S FAMILIES FIRST ACTION FUND
commidlist.append('C00491373') # AMERICA'S NEXT GENERATION LLC D/B/A THE NEXT GENERATION
commidlist.append('C00492322') # AMERICA'S PRESIDENT COMMITTEE
commidlist.append('C00492140') # AMERICAN BRIDGE 21ST CENTURY
commidlist.append('C00498725') # AMERICAN CITIZENS OF MODEST MEANS A COMM
commidlist.append('C00487363') # AMERICAN CROSSROADS
commidlist.append('C00488338') # AMERICAN DENTAL ASSOCIATION INDEPENDENT EXPENDITURES COMMITTEE
commidlist.append('C00502120') # AMERICAN FREEDOM AND GROWTH
commidlist.append('C00500512') # AMERICAN LEGACY ALLIANCE
commidlist.append('C00488759') # AMERICAN WORKER INC, THE
commidlist.append('C00498097') # AMERICANS FOR A BETTER TOMORROW, TOMORROW, INC.
commidlist.append('C00485821') # AMERICANS FOR NEW LEADERSHIP
commidlist.append('C00498261') # AMERICANS FOR RICK PERRY
commidlist.append('C00482620') # ARIZONANS WORKING TOGETHER
commidlist.append('C00500264') # BETTER TOMORROW SUPER PAC
commidlist.append('C00487827') # BLUE AMERICA PAC INDEPENDENT EXPENDITURE COMMITTEE
commidlist.append('C00499004') # BUCKET TEA PARTY POLITICAL ACTION COMMITTEE
commidlist.append('C00492553') # CALIFORNIA ASSOCIATION OF PHYSICIAN GROUPS (CAPG) PHYSICIANS INDEPENDENT EXPENDITURE COMMI
commidlist.append('C00484295') # CALIFORNIANS FOR FISCALLY CONSERVATIVE LEADERSHIP
commidlist.append('C00489617') # CAMPAIGN FOR AMERICAN VALUES PAC
commidlist.append('C00502849') # CAMPAIGN FOR PRIMARY ACCOUNTABILITY INC
commidlist.append('C00493718') # CARMEN'S LIST
commidlist.append('C00490862') # CARPENTERS DISTRICT COUNCIL OF KANSAS CITY AND VICINITY POLITICAL FUND
commidlist.append('C00494021') # CATHOLICVOTE.ORG CANDIDATE FUND
commidlist.append('C00502658') # CAUSEPAC
commidlist.append('C00497610') # CHRISTIANS UNITED SUPER PAC
commidlist.append('C00492215') # CHRISTINEPAC
commidlist.append('C00488767') # CITIZENS FOR A WORKING AMERICA PAC
commidlist.append('C00487199') # CITIZENS FOR ECONOMIC AND NATIONAL SECURITY
commidlist.append('C00488429') # CITIZENS FOR STRENGTH AND SECURITY PAC
commidlist.append('C00496927') # CITIZENS PROTEST NON PROFIT INC
commidlist.append('C00497420') # CITIZENS UNITED SUPER PAC LLC
commidlist.append('C00487470') # CLUB FOR GROWTH ACTION
commidlist.append('C00485011') # CLUB FOR GROWTH ADVOCACY INC
commidlist.append('C00488569') # COALITION TO PROTECT AMERICAN VALUES
commidlist.append('C00488486') # COMMUNICATIONS WORKERS OF AMERICA WORKING VOICES
commidlist.append('C00488437') # CONCERNED TAXPAYERS OF AMERICA
commidlist.append('C00502559') # CONSERVATIVE NATIONAL COMMITTEE
commidlist.append('C00487280') # CONSERVATIVES FOR TRUTH
commidlist.append('C00492116') # COOPERATIVE OF AMERICAN PHYSICIANS IE COMMITTEE
commidlist.append('C00494997') # DOWNTOWN FOR DEMOCRACY INDEPENDENT EXPENDITURE COMMITTEE
commidlist.append('C00496133') # DRAFT CHRISTIE FOR PRESIDENT INC
commidlist.append('C00502815') # ECONOMIC STRATEGY GROUP
commidlist.append('C00490409') # EMERGENCY COMMITTEE FOR ISRAEL PAC
commidlist.append('C00489856') # ENDING SPENDING FUND
commidlist.append('C00490664') # ENVIRONMENT COLORADO ACTION COMMITTEE
commidlist.append('C00489625') # FAITH FAMILY FREEDOM FUND
commidlist.append('C00502112') # FLORIDA FREEDOM AND GROWTH
commidlist.append('C00486688') # FLORIDA IS NOT FOR SALE
commidlist.append('C00490631') # FRACK ACTION USA PAC
commidlist.append('C00502641') # FREEDOM AND LIBERTY PAC
commidlist.append('C00498519') # FREEDOM BORN FUND
commidlist.append('C00496372') # FREEDOM FRONTIER ACTION FUND
commidlist.append('C00492504') # FREEDOM PATH ACTION NETWORK
commidlist.append('C00499020') # FREEDOMWORKS FOR AMERICA
commidlist.append('C00363390') # FRIENDS FOR A DEMOCRATIC WHITE HOUSE PAC INC
commidlist.append('C00498592') # FRIENDS FOR DEMOCRACY IN LIBYA
commidlist.append('C00498832') # GOVERNMENT INTEGRITY FUND ACTION NETWORK; THE
commidlist.append('C00490292') # GROW PAC
commidlist.append('C00487785') # HEADQUARTERS CMTE W HOLLYWOOD/BEV HILLS/STONEWALL DEM CLUB/STONEWALL YOUNG DEMS LTD
commidlist.append('C00491944') # HEARTLAND EMPOWERED ACTION FUND
commidlist.append('C00495028') # HOUSE MAJORITY PAC
commidlist.append('C00497727') # INDEPENDENT SOURCE PAC
commidlist.append('C00502971') # INDYAMERICANS.COM
commidlist.append('C00497941') # JOBS FOR FLORIDA
commidlist.append('C00497958') # JOBS FOR IOWA
commidlist.append('C00497966') # JOBS FOR SOUTH CAROLINA
commidlist.append('C00499525') # KEEP CONSERVATIVES UNITED
commidlist.append('C00478420') # LANTERN PROJECT, THE
commidlist.append('C00486845') # LEAGUE OF CONSERVATION VOTERS VICTORY FUND
commidlist.append('C00502963') # LEGISLATING EFFECTIVE AMERICAN DEMOCRACY
commidlist.append('C00490706') # LET FREEDOM RING AMERICA POLITICAL ACTION COMMITTEE
commidlist.append('C00490136') # LINCOLN CLUB OF ORANGE COUNTY FEDERAL IE COMMITTEE; THE
commidlist.append('C00485854') # LOUISIANA TRUTH PAC
commidlist.append('C00487736') # MAJORITY ACTION PAC
commidlist.append('C00484642') # MAJORITY PAC
commidlist.append('C00499731') # MAKE US GREAT AGAIN, INC
commidlist.append('C00501247') # MEN AGAINST PROSTITUTION AND TRAFFICKING
commidlist.append('C00494799') # MY AMERICA INC
commidlist.append('C00488742') # NATIONAL ASSOCIATION OF REALTORS CONGRESSIONAL FUND
commidlist.append('C00437822') # NATIONAL CAMPAIGN FUND
commidlist.append('C00490375') # NATIONAL NURSES UNITED FOR PATIENT PROTECTION
commidlist.append('C00489815') # NEA ADVOCACY FUND
commidlist.append('C00503086') # NEW HOPE PAC
commidlist.append('C00488940') # NEW HOUSE INDEPENDENT EXPENDITURE COMMITTEE
commidlist.append('C00489252') # NEW POWER PAC
commidlist.append('C00488494') # NEW PROSPERITY FOUNDATION; THE
commidlist.append('C00490656') # NO 2 SIDES PAC
commidlist.append('C00500868') # NO MERCY SUPER PAC
commidlist.append('C00490383') # OHIO STATE TEA PARTY; THE
commidlist.append('C00501098') # OUR DESTINY PAC
commidlist.append('C00490433') # OUR FUTURE OHIO PAC
commidlist.append('C00497412') # OUR VOICE PAC
commidlist.append('C00490219') # PARTNERSHIP FOR AMERICA'S FUTURE
commidlist.append('C00469890') # PATRIOT MAJORITY PAC
commidlist.append('C00498352') # PATRIOTS FOR A BETTER AMERICA PAC
commidlist.append('C00490896') # PATRIOTS FUND
commidlist.append('C00487025') # PEACH TEA PAC
commidlist.append('C00486878') # PEOPLE'S MAJORITY
commidlist.append('C00489799') # PLANNED PARENTHOOD VOTES
commidlist.append('C00467225') # PLAYOFF PAC, INC.
commidlist.append('C00495861') # PRIORITIES USA ACTION
commidlist.append('C00489765') # PROGRESSOHIO PAC
commidlist.append('C00489914') # PROTECT ALASKA'S FUTURE
commidlist.append('C00483883') # PROTECTING AMERICA'S RETIREES
commidlist.append('C00488502') # PROTECTING CHOICE IN CALIFORNIA 2010, A PROJECT OF PLANNED PARENTHOOD AFFILIATES OF CA
commidlist.append('C00493643') # RAISING RED ACTION FUND
commidlist.append('C00502369') # REBUILDING AMERICA
commidlist.append('C00497438') # REMOVE WEINER SUPPORT ERIC ULRICH FOR CONGRESS DRAFT COMMITTEE
commidlist.append('C00496349') # REPUBLICAN SUPER PAC INC
commidlist.append('C00489807') # RESTORE AMERICA'S VOICE PAC
commidlist.append('C00492173') # RESTORE OUR AMERICA POLITICAL ACTION COMMITTEE
commidlist.append('C00490045') # RESTORE OUR FUTURE, INC.
commidlist.append('C00503870') # RETHINK PAC
commidlist.append('C00499335') # REVOLUTION PAC
commidlist.append('C00490730') # RGA OHIO PAC
commidlist.append('C00494419') # SAVING FLORIDA'S FUTURE
commidlist.append('C00483693') # SIERRA CLUB INDEPENDENT ACTION
commidlist.append('C00497032') # SMALL BUSINESS POLITICAL ALLIANCE POLITICAL ACTION COMMITTEE (SBPA PAC)
commidlist.append('C00488510') # SPEAK OUT FOR AMERICA PAC
commidlist.append('C00488783') # SPEECHNOW.ORG
commidlist.append('C00494195') # STOP PUBLIC UNIONS NOW PAC
commidlist.append('C00503078') # STRONG UTAH PAC
commidlist.append('C00489781') # SUPER PAC FOR AMERICA
commidlist.append('C00502377') # TEXANS FOR AMERICA'S FUTURE
commidlist.append('C00488403') # TEXAS TEA PARTY PATRIOTS PAC
commidlist.append('C00501619') # TRIPLE CROWN PROJECT INC
commidlist.append('C00423095') # TRUST IN SMALL BUSINESS POLITICAL ACTION COMMITTEE (TISB PAC)
commidlist.append('C00497461') # TURN RIGHT USA
commidlist.append('C00484253') # UNITED FOOD AND COMMERCIAL WORKERS INTERNATIONAL UNION WORKING FAMILIES ADVOCACY PROJECT
commidlist.append('C00489203') # UNITED MINE WORKERS OF AMERICA POWER PAC
commidlist.append('C00495929') # UNITED STATES TRANSPORTATION ENERGY AND TECHNOLOGY ALLIANCE PAC
commidlist.append('C00490649') # US ISRAEL FRIENDSHIP PAC
commidlist.append('C00499095') # VETERANS FOR RICK PERRY
commidlist.append('C00490912') # VIETNAMESE AMERICAN POLITICAL ACTION COMMITTEE (VADPAC)
commidlist.append('C00498485') # VIRGINIA TEA PARTY ALLIANCE PAC A DIV OF TEA PARTY ALLIANCE INC
commidlist.append('C00423467') # VOTE OUT INCUMBENTS FOR DEMOCRACY
commidlist.append('C00498741') # VOTERS FOR JUSTICE, INC. PAC
commidlist.append('C00489211') # WE LOVE USA PAC
commidlist.append('C00490359') # WE'RE NOT GOING BACK
commidlist.append('C00473918') # WOMEN VOTE!
commidlist.append('C00490193') # WORKING FAMILIES FOR HAWAII
commidlist.append('C00430876') # WORKING FOR US POLITICAL ACTION COMMITTEE INC
commidlist.append('C00490847') # WORKING FOR WORKING AMERICANS - FEDERAL ACCOUNT
commidlist.append('C00501023') # YOUNG REPUBLICANS FOR A BETTER FLORIDA
commidlist.append('C00435818') # YOUNG VOTERS
commidlist.append('C00002600') # JOHN D. DINGELL FOR CONGRESS
commidlist.append('C00012229') # ALASKANS FOR DON YOUNG INC.
commidlist.append('C00013128') # CONGRESSMAN WAXMAN CAMPAIGN COMMITTEE
commidlist.append('C00020974') # PETE STARK RE-ELECTION COMMITTEE
commidlist.append('C00026757') # FRIENDS OF CONGRESSMAN GEORGE MILLER
commidlist.append('C00037606') # NORM DICKS FOR CONGRESS
commidlist.append('C00051227') # CONGRESSMAN BILL YOUNG CAMPAIGN COMMITTEE
commidlist.append('C00078105') # KILDEE FOR CONGRESS COMMITTEE
commidlist.append('C00081356') # KEEP NICK RAHALL IN CONGRESS COMMITTEE
commidlist.append('C00083428') # SENSENBRENNER COMMITTEE
commidlist.append('C00088658') # DREIER FOR CONGRESS COMMITTEE
commidlist.append('C00090357') # LEWIS FOR CONGRESS COMMITTEE
commidlist.append('C00096412') # COMMITTEE TO REELECT CONGRESSMAN CHRIS SMITH
commidlist.append('C00107003') # CITIZENS FOR TOM PETRI
commidlist.append('C00116632') # HAL ROGERS FOR CONGRESS
commidlist.append('C00120683') # HALL FOR CONGRESS COMMITTEE (RALPH HALL - ROCKWALL, TEXAS)
commidlist.append('C00128868') # BARNEY FRANK FOR CONGRESS COMMITTEE
commidlist.append('C00140715') # HOYER FOR CONGRESS
commidlist.append('C00145862') # DAN BURTON FOR CONGRESS COMMITTEE
commidlist.append('C00147686') # BERMAN FOR CONGRESS
commidlist.append('C00151456') # ALAN MOLLOHAN FOR CONGRESS COMMITTEE
commidlist.append('C00154625') # KAPTUR FOR CONGRESS
commidlist.append('C00156612') # LEVIN FOR CONGRESS
commidlist.append('C00165241') # COMMITTEE TO ELECT GARY L. ACKERMAN, INC.
commidlist.append('C00166017') # FRIENDS OF FRANK WOLF
commidlist.append('C00166504') # VISCLOSKY FOR CONGRESS
commidlist.append('C00167585') # CITIZENS FOR WATERS
commidlist.append('C00172619') # DAVIS FOR CONGRESS/FRIENDS OF DAVIS
commidlist.append('C00194803') # GALLEGLY FOR CONGRESS
commidlist.append('C00195065') # THE CONGRESSMAN JOE BARTON COMMITTEE
commidlist.append('C00195628') # PRICE FOR CONGRESS
commidlist.append('C00196774') # THE MARKEY COMMITTEE
commidlist.append('C00197160') # TEXANS FOR LAMAR SMITH
commidlist.append('C00197285') # COMMITTEE TO RE-ELECT ED TOWNS
commidlist.append('C00198796') # COBLE FOR CONGRESS
commidlist.append('C00200865') # ED ROYCE FOR CONGRESS
commidlist.append('C00202176') # WILLIE CARTER FOR PRESIDENT COMMITTEE
commidlist.append('C00202416') # JOHN LEWIS FOR CONGRESS
commidlist.append('C00202523') # WALLY HERGER FOR CONGRESS COMMITTEE
commidlist.append('C00213512') # NANCY PELOSI FOR CONGRESS
commidlist.append('C00213611') # LOUISE SLAUGHTER RE-ELECTION COMMITTEE
commidlist.append('C00214999') # JERRY CARROLL COMMITTEE FOR PRESIDENT
commidlist.append('C00219881') # NITA LOWEY FOR CONGRESS
commidlist.append('C00223073') # FRIENDS FOR JIM MCDERMOTT
commidlist.append('C00224691') # COMMITTEE TO RE-ELECT CONGRESSMAN DANA ROHRABACHER
commidlist.append('C00225045') # DON PAYNE FOR CONGRESS
commidlist.append('C00226522') # RICHARD E NEAL FOR CONGRESS COMMITTEE
commidlist.append('C00226928') # PALLONE FOR CONGRESS
commidlist.append('C00229104') # DUNCAN FOR CONGRESS
commidlist.append('C00229377') # FRIENDS OF CLIFF STEARNS
commidlist.append('C00231092') # FALEOMAVAEGA FOR CONGRESS COMMITTEE
commidlist.append('C00236513') # ENGEL FOR CONGRESS
commidlist.append('C00237198') # FRIENDS OF JOHN BOEHNER
commidlist.append('C00238444') # COSTELLO FOR CONGRESS COMMITTEE
commidlist.append('C00238865') # FRIENDS OF ROSA DELAURO
commidlist.append('C00240986') # SERRANO FOR CONGRESS
commidlist.append('C00241349') # MORAN FOR CONGRESS
commidlist.append('C00243428') # ROB ANDREWS U.S. HOUSE COMMITTEE
commidlist.append('C00244335') # CITIZENS FOR ELEANOR HOLMES NORTON
commidlist.append('C00250720') # FRIENDS OF SAM JOHNSON
commidlist.append('C00250860') # CITIZENS FOR JOHN OLVER FOR CONGRESS
commidlist.append('C00251918') # PASTOR FOR ARIZONA
commidlist.append('C00252973') # DONALD A. MANZULLO FOR CONGRESS
commidlist.append('C00253187') # PETERSON FOR CONGRESS
commidlist.append('C00254185') # GENE GREEN CONGRESSIONAL CAMPAIGN
commidlist.append('C00254441') # FATTAH FOR CONGRESS
commidlist.append('C00254573') # EDDIE BERNICE JOHNSON FOR CONGRESS
commidlist.append('C00254581') # GUTIERREZ FOR CONGRESS
commidlist.append('C00255141') # FRIENDS OF JANE HARMAN
commidlist.append('C00255190') # BARTLETT FOR CONGRESS COMMITTEE
commidlist.append('C00256925') # BOBBY SCOTT FOR CONGRESS
commidlist.append('C00257121') # CITIZENS FOR RUSH
commidlist.append('C00257337') # KEN CALVERT FOR CONGRESS COMMITTEE
commidlist.append('C00257956') # BOB GOODLATTE FOR CONGRESS COMMITTEE
commidlist.append('C00258244') # BUCK MCKEON FOR CONGRESS
commidlist.append('C00258475') # ANNA ESHOO FOR CONGRESS
commidlist.append('C00258855') # VOLUNTEERS FOR SHIMKUS
commidlist.append('C00259143') # LUCILLE ROYBAL-ALLARD FOR CONGRESS
commidlist.append('C00260265') # WOOLSEY FOR CONGRESS
commidlist.append('C00260547') # BACHUS FOR CONGRESS COMMITTEE
commidlist.append('C00260604') # MEL WATT FOR CONGRESS COMMITTEE
commidlist.append('C00261388') # BOB FILNER FOR CONGRESS
commidlist.append('C00261958') # FRIENDS OF JACK KINGSTON
commidlist.append('C00265322') # FRIENDS OF CONGRESSMAN TIM HOLDEN
commidlist.append('C00266940') # SANFORD BISHOP FOR CONGRESS
commidlist.append('C00269340') # LOBIONDO FOR CONGRESS
commidlist.append('C00269837') # HASTINGS FOR CONGRESS
commidlist.append('C00271312') # COMMITTEE TO RE-ELECT NYDIA M. VELAZQUEZ TO CONGRESS
commidlist.append('C00272211') # PETE KING FOR CONGRESS COMMITTEE
commidlist.append('C00272633') # FRIENDS OF MAURICE HINCHEY
commidlist.append('C00272732') # FRIENDS OF CORRINE BROWN
commidlist.append('C00273169') # MALONEY FOR CONGRESS
commidlist.append('C00278457') # JACK FELLURE CAMPAIGN COMMITTEE
commidlist.append('C00279851') # FRIENDS OF BENNIE THOMPSON
commidlist.append('C00280537') # ROS-LEHTINEN FOR CONGRESS
commidlist.append('C00283051') # MICA FOR CONGRESS
commidlist.append('C00284174') # LATOURETTE FOR CONGRESS COMMITTEE
commidlist.append('C00285171') # RE-ELECT MCGOVERN COMMITTEE
commidlist.append('C00286187') # THORNBERRY FOR CONGRESS COMMITTEE
commidlist.append('C00286500') # DOGGETT FOR US CONGRESS
commidlist.append('C00286856') # FRIENDS OF DOC HASTINGS
commidlist.append('C00287045') # LATHAM FOR CONGRESS
commidlist.append('C00287904') # LEE, SHEILA JACKSON
commidlist.append('C00287912') # LUCAS FOR CONGRESS
commidlist.append('C00289603') # LOFGREN FOR CONGRESS
commidlist.append('C00289983') # WHITFIELD FOR CONGRESS COMMITTEE
commidlist.append('C00290064') # DOYLE FOR CONGRESS COMMITTEE
commidlist.append('C00290429') # FRIENDS OF FARR
commidlist.append('C00290825') # NADLER FOR CONGRESS
commidlist.append('C00299404') # FRELINGHUYSEN FOR CONGRESS
commidlist.append('C00300830') # BRIAN BILBRAY FOR CONGRESS
commidlist.append('C00301838') # STEVE CHABOT FOR CONGRESS
commidlist.append('C00302422') # RANGEL FOR CONGRESS
commidlist.append('C00302570') # BASS VICTORY COMMITTEE
commidlist.append('C00303305') # PETE SESSIONS FOR CONGRESS
commidlist.append('C00304667') # SUE MYRICK FOR CONGRESS
commidlist.append('C00304709') # ADAM SMITH FOR CONGRESS COMMITTEE
commidlist.append('C00305052') # WALTER JONES COMMITTEE
commidlist.append('C00305342') # COMMITTEE TO RE-ELECT RON PAUL
commidlist.append('C00305920') # JESSE JACKSON JR FOR CONGRESS
commidlist.append('C00306829') # MIKE MCINTYRE FOR CONGRESS
commidlist.append('C00307314') # BLUMENAUER FOR CONGRESS
commidlist.append('C00308742') # SHERMAN FOR CONGRESS
commidlist.append('C00309237') # THE REYES COMMITTEE, INC.
commidlist.append('C00310136') # FRIENDS OF JOE PITTS
commidlist.append('C00310318') # CUMMINGS FOR CONGRESS CAMPAIGN COMMITTEE
commidlist.append('C00310532') # KAY GRANGER CAMPAIGN FUND
commidlist.append('C00310896') # RUBEN HINOJOSA FOR CONGRESS
commidlist.append('C00311043') # BRADY FOR CONGRESS
commidlist.append('C00311639') # DIANA DEGETTE FOR CONGRESS
commidlist.append('C00312017') # KIND FOR CONGRESS COMMITTEE
commidlist.append('C00313247') # ROBERT ADERHOLT FOR CONGRESS
commidlist.append('C00313494') # STEVE ROTHMAN FOR NEW JERSEY, INC.
commidlist.append('C00313510') # PASCRELL FOR CONGRESS
commidlist.append('C00313684') # RUSH HOLT FOR CONGRESS
commidlist.append('C00316661') # BOSWELL FOR CONGRESS
commidlist.append('C00318196') # JOHN TIERNEY FOR CONGRESS
commidlist.append('C00318931') # FRIENDS OF CAROLYN MCCARTHY
commidlist.append('C00320457') # TEAM EMERSON FOR JO ANN EMERSON
commidlist.append('C00320754') # DONNA CHRISTENSEN CAMPAIGN
commidlist.append('C00325449') # FRIENDS OF JOE BACA
commidlist.append('C00325704') # RE-ELECT CONGRESSMAN KUCINICH COMMITTEE
commidlist.append('C00325738') # BERKLEY FOR SENATE
commidlist.append('C00326066') # CIRO RODRIGUEZ FOR CONGRESS
commidlist.append('C00326264') # COMMITTEE TO RE-ELECT LORETTA SANCHEZ
commidlist.append('C00326363') # MIKE THOMPSON FOR CONGRESS
commidlist.append('C00326629') # KLINE FOR CONGRESS
commidlist.append('C00326801') # TAMMY BALDWIN FOR SENATE
commidlist.append('C00327023') # SCHAKOWSKY FOR CONGRESS
commidlist.append('C00327742') # FRIENDS OF WEINER
commidlist.append('C00329292') # EDUCATION & OPPORTUNITY FUND II
commidlist.append('C00330084') # CHARLES A. GONZALEZ CONGRESSIONAL CAMPAIGN
commidlist.append('C00330142') # LARSON FOR CONGRESS
commidlist.append('C00330241') # JUDY BIGGERT FOR CONGRESS
commidlist.append('C00330811') # LEE TERRY FOR CONGRESS
commidlist.append('C00330894') # RYAN FOR CONGRESS
commidlist.append('C00331389') # FRIENDS OF LOIS CAPPS
commidlist.append('C00331397') # SIMPSON FOR CONGRESS
commidlist.append('C00331496') # GARY MILLER FOR CONGRESS
commidlist.append('C00331769') # BARBARA LEE FOR CONGRESS
commidlist.append('C00332890') # MARY BONO MACK COMMITTEE
commidlist.append('C00333427') # WALDEN FOR CONGRESS
commidlist.append('C00333740') # BOB BRADY FOR CONGRESS
commidlist.append('C00334706') # NAPOLITANO FOR CONGRESS
commidlist.append('C00336388') # CAPUANO FOR CONGRESS COMMITTEE
commidlist.append('C00337436') # INSLEE FOR CONGRESS
commidlist.append('C00338954') # CROWLEY FOR CONGRESS
commidlist.append('C00341719') # RANDY CROW FOR PRESIDENT
commidlist.append('C00343236') # CULBERSON FOR CONGRESS
commidlist.append('C00343376') # PEOPLE FOR PLATTS COMMITTEE
commidlist.append('C00343475') # TODD AKIN FOR SENATE
commidlist.append('C00343863') # ROGERS FOR CONGRESS
commidlist.append('C00343871') # SCHIFF FOR CONGRESS
commidlist.append('C00344671') # SUSAN DAVIS FOR CONGRESS
commidlist.append('C00344697') # LANGEVIN FOR CONGRESS
commidlist.append('C00344721') # MATHESON FOR CONGRESS
commidlist.append('C00345546') # CITIZENS TO ELECT RICK LARSEN
commidlist.append('C00345710') # MIKE ROSS FOR CONGRESS COMMITTEE
commidlist.append('C00346080') # CLAY JR. FOR CONGRESS
commidlist.append('C00346767') # DEBORAH FOR CONGRESS
commidlist.append('C00347260') # JEFF FLAKE FOR US SENATE INC
commidlist.append('C00347492') # TIBERI FOR CONGRESS
commidlist.append('C00347849') # SHELLEY MOORE CAPITO FOR CONGRESS
commidlist.append('C00349431') # REHBERG FOR CONGRESS
commidlist.append('C00350397') # MIKE PENCE COMMITTEE
commidlist.append('C00350421') # FRIENDS OF TIM JOHNSON
commidlist.append('C00350520') # ISSA FOR CONGRESS
commidlist.append('C00351379') # MIKE HONDA FOR CONGRESS
commidlist.append('C00352849') # CRENSHAW FOR CONGRESS CAMPAIGN
commidlist.append('C00354688') # MCCOLLUM FOR CONGRESS
commidlist.append('C00355461') # CANTOR FOR CONGRESS
commidlist.append('C00357434') # COMMITTEE TO ELECT LEYVA FOR U.S.CONGRESS
commidlist.append('C00358952') # STEVE ISRAEL FOR CONGRESS COMMITTEE
commidlist.append('C00359034') # GRAVES FOR CONGRESS
commidlist.append('C00364935') # BILL SHUSTER FOR CONGRESS
commidlist.append('C00365593') # CANDICE MILLER FOR CONGRESS
commidlist.append('C00365692') # FORBES FOR CONGRESS
commidlist.append('C00365841') # MCCOTTER CONGRESSIONAL COMMITTEE
commidlist.append('C00366757') # JEFF MILLER FOR CONGRESS
commidlist.append('C00366773') # JOHN SULLIVAN FOR CONGRESS, INC
commidlist.append('C00366948') # STEPHEN F. LYNCH FOR CONGRESS COMMITTEE
commidlist.append('C00367110') # COMMITTEE TO RE-ELECT TRENT FRANKS TO CONGRESS
commidlist.append('C00367821') # MICHAUD FOR CONGRESS
commidlist.append('C00367862') # MIKE ROGERS FOR CONGRESS
commidlist.append('C00368522') # JOE WILSON FOR CONGRESS COMMITTEE
commidlist.append('C00369470') # GEOFF DAVIS FOR CONGRESS
commidlist.append('C00369686') # COMMITTEE TO ELECT MADELEINE Z. BORDALLO
commidlist.append('C00369801') # DAVID SCOTT FOR CONGRESS
commidlist.append('C00369942') # ROBERT LEE PRESIDENT
commidlist.append('C00370056') # DEVIN NUNES CAMPAIGN COMMITTEE
commidlist.append('C00370783') # GINGREY FOR CONGRESS, INC.
commidlist.append('C00371203') # JOHN CARTER FOR CONGRESS
commidlist.append('C00371211') # BRAD MILLER FOR UNITED STATES CONGRESS
commidlist.append('C00371302') # TEXANS FOR HENRY CUELLAR CONGRESSIONAL CAMPAIGN
commidlist.append('C00372102') # JIM GERLACH FOR CONGRESS COMMITTEE
commidlist.append('C00372201') # TIM MURPHY FOR CONGRESS
commidlist.append('C00372532') # MICHAEL BURGESS FOR CONGRESS
commidlist.append('C00372722') # JAMES HART FOR CONGRESS
commidlist.append('C00373001') # CITIZENS FOR TURNER
commidlist.append('C00373464') # TIM RYAN FOR CONGRESS
commidlist.append('C00373563') # KING FOR CONGRESS
commidlist.append('C00374058') # A WHOLE LOT OF PEOPLE FOR GRIJALVA CONGRESSIONAL COMMITTEE
commidlist.append('C00374231') # ROB BISHOP FOR CONGRESS
commidlist.append('C00375220') # JO BONNER FOR CONGRESS COMMITTEE
commidlist.append('C00375618') # TIM BISHOP FOR CONGRESS
commidlist.append('C00376087') # MARIO DIAZ-BALART FOR CONGRESS
commidlist.append('C00376665') # COOPER FOR CONGRESS
commidlist.append('C00376673') # DUTCH RUPPERSBERGER FOR CONGRESS
commidlist.append('C00376749') # RODNEY ALEXANDER FOR CONGRESS INC.
commidlist.append('C00376939') # MARSHA BLACKBURN FOR CONGRESS, INC.
commidlist.append('C00379735') # COLE FOR CONGRESS
commidlist.append('C00383794') # FRIENDS OF DENNIS CARDOZA
commidlist.append('C00383828') # CONAWAY FOR CONGRESS
commidlist.append('C00384016') # NEUGEBAUER CONGRESSIONAL COMMITTEE
commidlist.append('C00384057') # COMMITTEE TO RE-ELECT LINDA SANCHEZ
commidlist.append('C00384735') # FRIENDS OF JOHN BARROW
commidlist.append('C00385773') # DEBBIE WASSERMAN SCHULTZ FOR CONGRESS
commidlist.append('C00386110') # SCOTT GARRETT FOR CONGRESS
commidlist.append('C00386276') # RUSS CARNAHAN IN CONGRESS COMMITTEE
commidlist.append('C00386532') # LOUIE GOHMERT FOR CONGRESS COMMITTEE
commidlist.append('C00386748') # VIRGINIA FOXX FOR CONGRESS
commidlist.append('C00386755') # PRICE FOR CONGRESS
commidlist.append('C00386847') # CHARLIE DENT FOR CONGRESS
commidlist.append('C00387126') # WESTMORELAND FOR CONGRESS
commidlist.append('C00389197') # ALLYSON SCHWARTZ FOR CONGRESS
commidlist.append('C00390476') # CATHY MCMORRIS RODGERS FOR CONGRESS
commidlist.append('C00390724') # WALBERG FOR CONGRESS
commidlist.append('C00390955') # LUNGREN FOR CONGRESS
commidlist.append('C00391029') # JIM COSTA FOR CONGRESS
commidlist.append('C00391243') # FRIENDS OF CONNIE MACK
commidlist.append('C00392670') # POE FOR CONGRESS
commidlist.append('C00392688') # MCCAUL FOR CONGRESS, INC
commidlist.append('C00393348') # KENNY MARCHANT FOR CONGRESS
commidlist.append('C00393512') # BEN CHANDLER FOR CONGRESS
commidlist.append('C00393629') # MCHENRY FOR CONGRESS
commidlist.append('C00393652') # DONNELLY FOR INDIANA
commidlist.append('C00394353') # CANSECO FOR CONGRESS
commidlist.append('C00394866') # CHARLES BOUSTANY JR. MD FOR CONGRESS, INC.
commidlist.append('C00394957') # SCALISE FOR CONGRESS
commidlist.append('C00395467') # JEFF FORTENBERRY FOR UNITED STATES CONGRESS
commidlist.append('C00395475') # MESPLAY FOR PRESIDENT
commidlist.append('C00395848') # CLEAVER FOR CONGRESS
commidlist.append('C00396028') # AL GREEN FOR CONGRESS
commidlist.append('C00397505') # MOORE FOR CONGRESS
commidlist.append('C00397737') # FRIENDS OF DAVE REICHERT
commidlist.append('C00398644') # MCNERNEY FOR CONGRESS
commidlist.append('C00401034') # HIGGINS FOR CONGRESS
commidlist.append('C00401190') # BUTTERFIELD FOR CONGRESS
commidlist.append('C00403154') # VANDENBERG FOR CONGRESS
commidlist.append('C00404335') # WILDES FOR CONGRESS
commidlist.append('C00405431') # DAN LIPINSKI FOR CONGRESS
commidlist.append('C00408534') # BILIRAKIS FOR CONGRESS
commidlist.append('C00409219') # MATSUI FOR CONGRESS
commidlist.append('C00409409') # TIM WALZ FOR US CONGRESS
commidlist.append('C00409441') # BRALEY FOR CONGRESS
commidlist.append('C00409797') # CONYERS FOR CONGRESS
commidlist.append('C00410118') # MICHELEBACHMANN.COM
commidlist.append('C00410233') # COURTNEY FOR CONGRESS
commidlist.append('C00410639') # PERLMUTTER FOR CONGRESS
commidlist.append('C00410647') # SCHMIDT FOR CONGRESS COMMITTEE
commidlist.append('C00410753') # SIRES FOR CONGRESS
commidlist.append('C00410761') # CASTOR FOR CONGRESS
commidlist.append('C00410829') # BOREN FOR CONGRESS
commidlist.append('C00410837') # HELLER FOR CONGRESS
commidlist.append('C00410969') # ROSKAM FOR CONGRESS COMMITTEE
commidlist.append('C00411660') # COMMITTEE TO ELECT CHRIS MURPHY
commidlist.append('C00412015') # FRIENDS OF CHARLIE WILSON
commidlist.append('C00412312') # JOHN CAMPBELL FOR CONGRESS
commidlist.append('C00412759') # VERN BUCHANAN FOR CONGRESS
commidlist.append('C00412890') # ADRIAN SMITH FOR CONGRESS
commidlist.append('C00413179') # WELCH FOR CONGRESS
commidlist.append('C00413310') # CITIZENS FOR ALTMIRE
commidlist.append('C00413393') # HEATH SHULER FOR CONGRESS
commidlist.append('C00414318') # LOEBSACK FOR CONGRESS
commidlist.append('C00414391') # CARNEY FOR CONGRESS
commidlist.append('C00414912') # IMPALER FOR PRESIDENT 2012; THE
commidlist.append('C00415182') # FRIENDS OF JOHN SARBANES
commidlist.append('C00415331') # CLARKE FOR CONGRESS
commidlist.append('C00416156') # KILROY FOR CONGRESS
commidlist.append('C00416594') # JIM JORDAN FOR CONGRESS
commidlist.append('C00416818') # ZACK SPACE FOR CONGRESS COMMITTEE
commidlist.append('C00417550') # FRIENDS OF DAN MAFFEI
commidlist.append('C00417618') # GIFFORDS FOR CONGRESS
commidlist.append('C00417816') # BETTY SUTTON FOR CONGRESS
commidlist.append('C00418293') # COMMITTEE TO RE-ELECT HENRY HANK JOHNSON
commidlist.append('C00419630') # YARMUTH FOR CONGRESS
commidlist.append('C00419978') # CAROL SHEA-PORTER FOR CONGRESS
commidlist.append('C00420745') # LAMBORN FOR CONGRESS
commidlist.append('C00420760') # FRIENDS OF MAZIE HIRONO
commidlist.append('C00420935') # KEVIN MCCARTHY FOR CONGRESS
commidlist.append('C00421339') # COLLEEN FOR CONGRESS
commidlist.append('C00422410') # ELLISON FOR CONGRESS
commidlist.append('C00422964') # DONNA EDWARDS FOR CONGRESS
commidlist.append('C00422980') # STEVE COHEN FOR CONGRESS
commidlist.append('C00423640') # PRESIDENT WARREN RODERICK ASHE
commidlist.append('C00424713') # COMMITTEE TO ELECT ALAN GRAYSON
commidlist.append('C00426742') # JTK FOR CONGRESS
commidlist.append('C00427708') # EDDIE ZAMORA FOR CONGRESS
commidlist.append('C00428417') # COMMITTEE TO ELECT JEFF DAVIS PRESIDENT IN 2012
commidlist.append('C00428987') # MALONE FOR US PRESIDENT 2012
commidlist.append('C00429514') # PRESIDENT EMPEROR CAESAR
commidlist.append('C00430991') # FRIENDS FOR GREGORY MEEKS
commidlist.append('C00431031') # FREDRICK EUGENE OGIN
commidlist.append('C00431502') # SWETT EXPLORATORY COMMITTEE
commidlist.append('C00431684') # FRIENDS OF JASON CHAFFETZ
commidlist.append('C00432013') # WILL BLAKLEY FOR PRESIDENT
commidlist.append('C00432088') # USA PRESIDENTIAL ELECTION COMMITTEE
commidlist.append('C00432740') # INTERIGATED REVIVAL
commidlist.append('C00432831') # WUENSCHE FOR PRESIDENT INC
commidlist.append('C00432906') # TOM ROONEY FOR CONGRESS
commidlist.append('C00432948') # MCGOFF FOR CONGRESS
commidlist.append('C00432955') # PAUL BROUN COMMITTEE
commidlist.append('C00433136') # THE NIKI TSONGAS COMMITTEE
commidlist.append('C00433391') # PINGREE FOR CONGRESS
commidlist.append('C00433524') # DUNCAN D. HUNTER FOR CONGRESS
commidlist.append('C00433730') # LYNN JENKINS FOR CONGRESS
commidlist.append('C00433763') # KISSELL FOR CONGRESS
commidlist.append('C00433821') # DEMMER FOR CONGRESS
commidlist.append('C00434191') # JIM HIMES FOR CONGRESS
commidlist.append('C00434563') # MARTIN HEINRICH FOR SENATE
commidlist.append('C00434571') # RICHARDSON FOR CONGRESS
commidlist.append('C00435065') # BOCCIERI FOR CONGRESS
commidlist.append('C00435099') # BILL FOSTER FOR CONGRESS COMMITTEE
commidlist.append('C00435370') # FRIENDS OF JARED POLIS COMMITTEE
commidlist.append('C00435636') # PIERLUISI 2008, INC.
commidlist.append('C00435974') # ANDY HARRIS FOR CONGRESS
commidlist.append('C00436758') # BILL HEDRICK FOR CONGRESS
commidlist.append('C00437293') # KIRKPATRICK FOR ARIZONA
commidlist.append('C00437673') # LAURA JANE MCCUMBER POLITICAL CAMPAIGN COMMITTEE
commidlist.append('C00437756') # SCHOCK FOR CONGRESS
commidlist.append('C00437889') # PETERS FOR CONGRESS
commidlist.append('C00437913') # OLSON FOR CONGRESS COMMITTEE
commidlist.append('C00438697') # LATTA FOR CONGRESS
commidlist.append('C00438705') # SOLE ROYAL EMBASSY OF THE UNITED STATES OF TURTLE ISLAND; THE
commidlist.append('C00439091') # J E W KENNEDY BANKS FOR PRESIDENT COMMITTEE
commidlist.append('C00439661') # FRIENDS OF ERIK PAULSEN
commidlist.append('C00439737') # GREG MARTIN 2012 PRESIDENTIAL CAMPAIGN COMMITTEE
commidlist.append('C00440016') # HALVORSON FOR CONGRESS
commidlist.append('C00440115') # STEVE AUSTRIA FOR CONGRESS
commidlist.append('C00441014') # ROB WITTMAN FOR CONGRESS
commidlist.append('C00441212') # PHILLIPS FOR CONGRESS
commidlist.append('C00441295') # GREGG HARPER FOR CONGRESS
commidlist.append('C00441352') # STIVERS FOR CONGRESS
commidlist.append('C00441840') # FAULK FOR CONGRESS
commidlist.append('C00442921') # ANDRE CARSON FOR CONGRESS
commidlist.append('C00443580') # LUMMIS FOR CONGRESS
commidlist.append('C00443689') # PEOPLE FOR BEN
commidlist.append('C00443705') # JACKIE SPEIER FOR CONGRESS
commidlist.append('C00444224') # LANCE FOR CONGRESS
commidlist.append('C00444471') # CITIZENS TO ELECT PHIL ROE TO CONGRESS
commidlist.append('C00444620') # FRIENDS OF GLENN THOMPSON
commidlist.append('C00444968') # FRIENDS OF BILL POSEY
commidlist.append('C00445015') # FLEMING FOR CONGRESS
commidlist.append('C00445023') # GUTHRIE FOR CONGRESS
commidlist.append('C00445122') # LOU BARLETTA FOR CONGRESS
commidlist.append('C00445148') # GEORGE WASHINGTON WILLIAMS COMMITTEE
commidlist.append('C00445452') # CONNOLLY FOR CONGRESS
commidlist.append('C00446526') # KEN CROSS FOR PRESIDENT
commidlist.append('C00446815') # MCCLINTOCK FOR CONGRESS
commidlist.append('C00446906') # KURT SCHRADER FOR CONGRESS
commidlist.append('C00450049') # PAUL TONKO FOR CONGRESS
commidlist.append('C00450148') # CHRIS LEE FOR CONGRESS
commidlist.append('C00451005') # RICHARD HANNA FOR CONGRESS COMMITTEE
commidlist.append('C00451146') # HERB ROBINSON COMMITTEE, INC
commidlist.append('C00451336') # RICHMOND FOR CONGRESS
commidlist.append('C00451807') # BILL CASSIDY FOR CONGRESS
commidlist.append('C00452185') # COMMITTEE TO ELECT THOMAS ROBERT STEVENS PRESIDENT
commidlist.append('C00452540') # REGGIE FOR PRESIDENT
commidlist.append('C00452995') # POSTMA FOR CONGRESS
commidlist.append('C00454694') # MARCIA FUDGE FOR CONGRESS
commidlist.append('C00457556') # QUIGLEY FOR CONGRESS
commidlist.append('C00457960') # MICHAEL WILLIAMS FOR CONGRESS
commidlist.append('C00458125') # JUDY CHU FOR CONGRESS
commidlist.append('C00458604') # VIRGINIANS FOR CHUCK SMITH
commidlist.append('C00458679') # BLAINE FOR CONGRESS 2012
commidlist.append('C00458877') # KINZINGER FOR CONGRESS
commidlist.append('C00458976') # TERRI SEWELL FOR CONGRESS
commidlist.append('C00459255') # FRIENDS OF TODD YOUNG
commidlist.append('C00459297') # HUIZENGA FOR CONGRESS
commidlist.append('C00459354') # BOBBY SCHILLING FOR CONGRESS
commidlist.append('C00459842') # FRIENDS OF STEVE POUGNET
commidlist.append('C00459909') # JOHN WALTZ FOR CONGRESS
commidlist.append('C00460055') # FREDERICA S. WILSON FOR CONGRESS
commidlist.append('C00460063') # BILLY LONG FOR CONGRESS
commidlist.append('C00460329') # GREENSPON 2012 PRESIDENTIAL COMMITTEE
commidlist.append('C00460402') # POMPEO FOR CONGRESS INC
commidlist.append('C00460667') # LUKE MESSER FOR CONGRESS
commidlist.append('C00460683') # HANKINS FOR CONGRESS
commidlist.append('C00460808') # KELLY FOR CONGRESS
commidlist.append('C00460899') # JOHN CARNEY FOR CONGRESS
commidlist.append('C00460923') # FRIENDS OF JOHN LOUGHLIN
commidlist.append('C00461012') # DARIA NOVAK FOR CONGRESS
commidlist.append('C00461053') # BERNIER FOR CONGRESS
commidlist.append('C00461061') # BERA FOR CONGRESS
commidlist.append('C00461350') # FRIENDS OF FRANK GUINTA
commidlist.append('C00461806') # PAUL GOSAR FOR CONGRESS
commidlist.append('C00461822') # CHUCK FLEISCHMANN FOR CONGRESS COMMITTEE, INC.
commidlist.append('C00462010') # MILLER FOR PRESIDENT
commidlist.append('C00462143') # MARTHA ROBY FOR CONGRESS
commidlist.append('C00462168') # CONSTITUTIONIST FKA WE THE PEOPLE FOR THE PEOPLE VOICE OF AMERICA
commidlist.append('C00462374') # CRAWFORD FOR CONGRESS
commidlist.append('C00462390') # 007 GO GODWIN COMMITTEE
commidlist.append('C00462515') # YOST FOR CONGRESS
commidlist.append('C00462523') # TREY GOWDY FOR CONGRESS
commidlist.append('C00462663') # COMMITTEE TO ELECT JOHN PISTONE
commidlist.append('C00462697') # GARAMENDI FOR CONGRESS
commidlist.append('C00462853') # DOHENY FOR CONGRESS
commidlist.append('C00462861') # KUSTER FOR CONGRESS, INC.
commidlist.append('C00462911') # SPRADLIN FOR CONGRESS 2012
commidlist.append('C00463406') # MORGAN FOR CONGRESS
commidlist.append('C00463463') # JEFF BOSS FOR PRESIDENT
commidlist.append('C00463570') # ROCKY FOR CONGRESS 2012
commidlist.append('C00463620') # RIBBLE FOR CONGRESS
commidlist.append('C00463638') # CITIZENS FOR NUCIFORO
commidlist.append('C00463687') # SCOTT RIGELL FOR CONGRESS
commidlist.append('C00463836') # PEOPLE FOR PEARCE
commidlist.append('C00463927') # TOM CRAMER FOR CONGRESS
commidlist.append('C00464032') # TOM REED FOR CONGRESS
commidlist.append('C00464073') # FRIENDS OF SCOTT DESJARLAIS
commidlist.append('C00464149') # MOBROOKSFORCONGRESS.COM
commidlist.append('C00464305') # TOWNE FOR CONGRESS
commidlist.append('C00464339') # DUFFY FOR CONGRESS
commidlist.append('C00464354') # BILL HUDAK FOR CONGRESS
commidlist.append('C00464487') # NUNNELEE FOR CONGRESS
commidlist.append('C00464495') # BILL OWENS FOR CONGRESS
commidlist.append('C00464669') # ED MARTIN FOR CONGRESS
commidlist.append('C00465054') # FRANK SCATURRO FOR CONGRESS
commidlist.append('C00465096') # RANDALL FOR CONGRESS COMMITTEE
commidlist.append('C00465187') # DR DONNA CAMPBELL FOR CONGRESS
commidlist.append('C00465245') # RANDY ALTSCHULER FOR CONGRESS
commidlist.append('C00465443') # CAMPAIGN COMMITTEE FOR WHENCE BROWN FOR PRESIDENT FNA GINA MAY ROCHE BROWN
commidlist.append('C00465971') # DOLD FOR CONGRESS
commidlist.append('C00466359') # JIM RENACCI FOR CONGRESS
commidlist.append('C00466425') # COZAD FOR CONGRESS
commidlist.append('C00466482') # FAMILIES FOR JAMES LANKFORD
commidlist.append('C00466490') # FRIENDS OF NAN HAYWORTH
commidlist.append('C00466508') # BERRYHILL FOR CONGRESS
commidlist.append('C00466516') # GIBBS FOR CONGRESS
commidlist.append('C00466607') # TRIVEDI FOR CONGRESS
commidlist.append('C00466821') # COMMITTEE TO ELECT MICHAEL STOLLAIRE PRESIDENT
commidlist.append('C00466870') # PAT MEEHAN FOR CONGRESS
commidlist.append('C00467522') # RANDY HULTGREN FOR CONGRESS
commidlist.append('C00467530') # CITIZENS FOR ROTHFUS INC.
commidlist.append('C00467571') # ANDY BARR FOR CONGRESS, INC.
commidlist.append('C00467597') # RICHARD KLINE FOR PRESIDENT
commidlist.append('C00467613') # BATES FOR CONGRESS COMMITTEE
commidlist.append('C00468116') # RE-ELECT TIM GRIFFIN FOR CONGRESS COMMITTEE
commidlist.append('C00468256') # BUCSHON FOR CONGRESS
commidlist.append('C00468405') # ROBERT HURT FOR CONGRESS
commidlist.append('C00468421') # FRIENDS OF JOE HECK
commidlist.append('C00468454') # FRIENDS OF COLONEL PETE STIGLICH
commidlist.append('C00468488') # SHANNON ROBERTS FOR CONGRESS
commidlist.append('C00468579') # WALORSKI FOR CONGRESS INC
commidlist.append('C00468777') # CECIL FOR CONGRESS COMMITTEE
commidlist.append('C00468959') # SOUTHERLAND FOR CONGRESS
commidlist.append('C00469163') # TED DEUTCH FOR CONGRESS COMMITTEE
commidlist.append('C00469882') # KILILI FOR CONGRESS
commidlist.append('C00470179') # DR DAN 4 CONGRESS 2012
commidlist.append('C00470245') # JAY CLOUGH FOR CONGRESS
commidlist.append('C00470757') # VOTETIPTON.COM
commidlist.append('C00470807') # MICHAEL GRIMM FOR CONGRESS
commidlist.append('C00470864') # VOTE GEORGE COOPER INC
commidlist.append('C00470948') # RAUL LABRADOR FOR IDAHO
commidlist.append('C00471128') # BENNING FOR CONGRESS
commidlist.append('C00471177') # FRIENDS OF JAMES ROACH
commidlist.append('C00471367') # HEUPEL FOR PRESIDENT
commidlist.append('C00471474') # CITIZENS FOR WATKINS
commidlist.append('C00471680') # SUMMER SHIELDS FOR CONGRESS
commidlist.append('C00471896') # RENEE ELLMERS FOR CONGRESS COMMITTEE
commidlist.append('C00472050') # AMERICANS FOR MURRAY
commidlist.append('C00472159') # DENNY HECK FOR CONGRESS
commidlist.append('C00472316') # GAULRAPP 4 CONGRESS
commidlist.append('C00472365') # YODER FOR CONGRESS
commidlist.append('C00472704') # JAIME FOR CONGRESS
commidlist.append('C00473272') # DENHAM FOR CONGRESS
commidlist.append('C00473421') # ROSE IZZO FOR CONGRESS
commidlist.append('C00473751') # ANN MARIE BUERKLE FOR CONGRESS
commidlist.append('C00473777') # COMMITTEE TO ELECT STEPHEN A. LABATE, INC.
commidlist.append('C00473868') # GIGLIOTTI FOR CONGRESS
commidlist.append('C00474064') # KURT KELLY FOR CONGRESS
commidlist.append('C00474189') # MIKE KELLY FOR CONGRESS
commidlist.append('C00474254') # PARKER FOR CONGRESS
commidlist.append('C00474288') # MERVPAC
commidlist.append('C00474452') # BYBERG FOR CONGRESS
commidlist.append('C00474478') # KAREN HARRINGTON FOR CONGRESS, INC.
commidlist.append('C00474494') # SINGLETON FOR PRESIDENT
commidlist.append('C00474528') # COMMITTEE TO ELECT CHARLES BLACK FOR CONGRESS
commidlist.append('C00474619') # BERG FOR CONGRESS
commidlist.append('C00474668') # LURIE FOR CONGRESS 2012
commidlist.append('C00475004') # PANTANO FOR NC COMMITTEE
commidlist.append('C00475103') # FITZPATRICK FOR CONGRESS
commidlist.append('C00475145') # MARINO FOR CONGRESS
commidlist.append('C00475285') # MCCALL FOR PRESIDENT IN 2012
commidlist.append('C00475632') # CRAVAACK FOR CONGRESS CAMPAIGN COMMITTEE
commidlist.append('C00475863') # QUAYLE FOR CONGRESS
commidlist.append('C00476044') # LINGENFELDER FOR CONGRESS CAMPAIGN
commidlist.append('C00476176') # VOTERS FOR DICK MURI
commidlist.append('C00476192') # HOOSIERS FOR ROKITA, INC.
commidlist.append('C00476226') # TIM SCOTT FOR CONGRESS
commidlist.append('C00476291') # JUSTIN AMASH FOR CONGRESS
commidlist.append('C00476325') # BENISHEK FOR CONGRESS, INC.
commidlist.append('C00476523') # KAREN BASS FOR CONGRESS
commidlist.append('C00476564') # CICILLINE COMMITTEE
commidlist.append('C00476598') # FRIENDS OF SEAN BIELAT
commidlist.append('C00476820') # BILL JOHNSON FOR CONGRESS COMMITTEE
commidlist.append('C00476853') # KRISTI FOR CONGRESS
commidlist.append('C00476861') # MARK CRITZ FOR CONGRESS COMMITTEE
commidlist.append('C00477240') # MORGAN GRIFFITH FOR CONGRESS
commidlist.append('C00477356') # DAVID RIVERA FOR CONGRESS
commidlist.append('C00477422') # COMMITTEE TO ELECT MIKE STAHLY
commidlist.append('C00477661') # JON RUNYAN FOR CONGRESS, INC
commidlist.append('C00477745') # WOMACK FOR CONGRESS COMMITTEE
commidlist.append('C00477828') # HANSEN CLARKE FOR CONGRESS
commidlist.append('C00477984') # CHRIS GIBSON FOR CONGRESS
commidlist.append('C00478164') # TOM WATSON FOR CONGRESS
commidlist.append('C00478503') # OLIVERIO FOR CONGRESS
commidlist.append('C00478636') # BETH ANNE RANKIN FOR CONGRESS
commidlist.append('C00479030') # KOLB 4 CONGRESS
commidlist.append('C00479063') # THE BILL KEATING COMMITTEE
commidlist.append('C00479188') # ANTHONY PORTANTINO CONGRESSIONAL EXPLORATORY COMMITTEE
commidlist.append('C00479303') # MARK ROSEN FOR CONGRESS
commidlist.append('C00479444') # RUTHERFORD B HAYES FOR PRESIDENT 2012
commidlist.append('C00480103') # CITIZENS FOR OLIVIA FOR CONGRESS
commidlist.append('C00480608') # SCHONBERG FOR CONGRESS
commidlist.append('C00480657') # MOSHEH FOR PRESIDENT
commidlist.append('C00481259') # RICK WAUGH FOR CONGRESS
commidlist.append('C00481333') # DAVID LUTRIN FOR CONGRESS
commidlist.append('C00481341') # ART ROBINSON FOR CONGRESS
commidlist.append('C00481523') # RAPHAEL HERMAN FOR PRESIDENT THE UNITED STATES OF AMERICA
commidlist.append('C00481655') # JESSE YOUNG FOR US CONGRESS
commidlist.append('C00481911') # DANIEL WEBSTER FOR CONGRESS
commidlist.append('C00482307') # ROB WOODALL FOR CONGRESS
commidlist.append('C00482406') # SCHRINER PRESIDENTIAL ELECTION COMMITTEE
commidlist.append('C00482737') # AUSTIN SCOTT FOR CONGRESS INC
commidlist.append('C00482927') # DEONIA NEVEU A REAL VOTE FOR THE PEOPLE
commidlist.append('C00483529') # JOEL BALAM FOR CONGRESS COMMITTEE
commidlist.append('C00483784') # MCDOWELL FOR CONGRESS
commidlist.append('C00484170') # PRAETORIAN PARTY; THE
commidlist.append('C00484675') # IT'S THE FULL THE UNITED STATES OF THE AMERICA ORIGINAL
commidlist.append('C00484683') # STUTZMAN FOR CONGRESS
commidlist.append('C00484774') # BECKER FOR CONGRESS
commidlist.append('C00484907') # HERMAN FOR PRESIDENT
commidlist.append('C00485029') # FRIENDS OF DENNIS KNILL FOR PRESIDENT
commidlist.append('C00485284') # GERRY DEMBROWSKI PAC
commidlist.append('C00485409') # MATT STRITTMATTER COMMITTEE
commidlist.append('C00485458') # NICKOLAS CUEVAS 2012
commidlist.append('C00485607') # TANNER CLINE MCCUMBER BUSH POLITICAL CAMPAIGN FUND
commidlist.append('C00485656') # SAVANNAH JEWEL MCCUMBER BUSH POLITICAL CAMPAIGN FUND
commidlist.append('C00486001') # GEORGE BAILEY FOR PRESIDENT 2012
commidlist.append('C00486266') # PAUL RUSSELL ROSENBERGER PRES USA 2012 TO BUILD A BEAUTIFUL WORLD AT PEACE POLLUTION FREE
commidlist.append('C00486506') # JIMENEZ FOR PRESIDENT 2012
commidlist.append('C00487413') # JAMES KOCH FOR US PRESIDENT 2012
commidlist.append('C00487728') # DANY LAPORTE COMMITTEE
commidlist.append('C00487983') # DIVINE TRANQUILITY
commidlist.append('C00488635') # FRIENDS OF JAMES GREY 2012
commidlist.append('C00489195') # YINKA ABOSEDE ADESHINA
commidlist.append('C00489633') # JOHN DAVIS FOR PRESIDENT
commidlist.append('C00489666') # ANDREW HASTINGS GIMP FOR PRESIDENT
commidlist.append('C00489955') # HENRY YANEZ FOR CONGRESS
commidlist.append('C00490060') # COMMITTEE TO ELECT DAN W ROZELLE PRESIDENT
commidlist.append('C00490490') # COMMITTEE TO ELECT VANESSA MCGEE SMITH KEARNEY FOR CONGRESS&PUT RUAL NC BACK TO WORK; THE
commidlist.append('C00490797') # FRIENDS OF KURT BRADBURN
commidlist.append('C00490938') # SAVIOR PRESIDENTIAL COMMITTEE (USA) 2012
commidlist.append('C00491035') # COMMITTEE TO ELECT R. KENNETH JONES, PRESIDENT OF THE UNITED STATES OF AMERICA
commidlist.append('C00491258') # BILL LAWRENCE FOR CONGRESS
commidlist.append('C00491308') # COMMITTEE TO EXPLORE ELECTING DAN MORENOFF TO CONGRESS IN 2012
commidlist.append('C00491357') # STEVE DAINES FOR MONTANA
commidlist.append('C00491399') # COMMITTEE TO ELECT JIM RUNDBERG
commidlist.append('C00491498') # JOHN R HOELZEL JR FOR PRESIDENT OF THE UNITED STATES
commidlist.append('C00491662') # JIM RILEY FOR CONGRESS
commidlist.append('C00491746') # HUFFMAN FOR CONGRESS 2012 EXPLORATORY COMMITTEE
commidlist.append('C00491902') # ARAGON FOR PRESIDENT 2012
commidlist.append('C00492009') # CESAR CISNEROS FOR PRESIDENT OF THE UNITED STATES OF AMERICA
commidlist.append('C00492017') # TUBBS4PRESIDENT2012
commidlist.append('C00492199') # PEOPLE FOR DAVID A LARSON
commidlist.append('C00492272') # NICK GARZILLI FOR CONGRESS
commidlist.append('C00492330') # NICHOLAS RUIZ III FOR CONGRESS
commidlist.append('C00492371') # RANDALL TERRY FOR PRESIDENT CAMPAIGN COMMITTEE
commidlist.append('C00492413') # SCHWEIKERT FOR CONGRESS
commidlist.append('C00492447') # MICHAEL J MANLEY FOR PRESIDENT 2012
commidlist.append('C00492454') # GARDNER FOR CONGRESS 2012
commidlist.append('C00492470') # SAUCEDO MERCER FOR CONGRESS
commidlist.append('C00492488') # KREEGEL FOR CONGRESS
commidlist.append('C00492496') # SPIRIT OF 1854 COMMITTEE TO ELECT DAVE ANDERSON
commidlist.append('C00492546') # DENAME, MICHAEL JR
commidlist.append('C00492694') # RAMOS FOR AMERICA
commidlist.append('C00492702') # VAUGHN FOR CONGRESS
commidlist.append('C00492710') # PARMELE FOR PRESIDENT
commidlist.append('C00492744') # JOHN DUMMETT FOR PRESIDENT COMMITTEE
commidlist.append('C00492777') # JERRY NOLTE FOR CONGRESS
commidlist.append('C00492793') # ROGER GOODMAN FOR CONGRESS
commidlist.append('C00492801') # JOHNSON2012
commidlist.append('C00492835') # TIM KALEMKARIAN H12 COMMITTEE
commidlist.append('C00492892') # TIM KALEMKARIAN P16 COMMITTEE
commidlist.append('C00492900') # KIS PARTY OF WASHINGTON STATE
commidlist.append('C00492918') # RIPPEON FOR CONGRESS INC
commidlist.append('C00492934') # NYREN FOR CONGRESS
commidlist.append('C00492959') # ANDY MARTIN CAMPAIGN COMMITTEE
commidlist.append('C00492967') # COMMITTEE TO ELECT MATTHEW WOODMANCY
commidlist.append('C00493114') # COMMITEE TO BUILD DOME HOMES
commidlist.append('C00493155') # JOHN FOLEY FOR CONGRESS
commidlist.append('C00493171') # CHUCK GRAY FOR CONGRESS
commidlist.append('C00493189') # FRANKE FOR CONGRESS
commidlist.append('C00493247') # ATKINSON FOR CONGRESS
commidlist.append('C00493379') # ABEL MALDONADO FOR CONGRESS
commidlist.append('C00493395') # MARK GREENBERG FOR CONGRESS
commidlist.append('C00493403') # RICKY GILL FOR CONGRESS
commidlist.append('C00493692') # BUDDY ROEMER FOR PRESIDENT, INC.
commidlist.append('C00493825') # FRIENDS OF PATRICK MURPHY
commidlist.append('C00493866') # ERIC MALONEY FOR CONGRESS
commidlist.append('C00493965') # KUCHAR FOR US HOUSE COMMITTEE
commidlist.append('C00493973') # KEVIN NELSON 2012
commidlist.append('C00494096') # DAN ROBERTI FOR CONGRESS
commidlist.append('C00494203') # FRIENDS OF ELIZABETH ESTY
commidlist.append('C00494310') # KAREN DIEBEL FOR CONGRESS 2012
commidlist.append('C00494377') # POLITICAL CAMPAIGN TO ELECT KP GEORGE
commidlist.append('C00494443') # FRED KARGER FOR PRESIDENT
commidlist.append('C00494575') # CALDER FOR CONGRESS 2012
commidlist.append('C00494583') # TED YOHO FOR CONGRESS
commidlist.append('C00494591') # NIZ KAMAL FOR CONGRESS
commidlist.append('C00494773') # TERRY WHITE FOR INDIANA
commidlist.append('C00494815') # MARTY KNOLLENBERG FOR CONGRESS
commidlist.append('C00494823') # JARED BLANKENSHIP FOR PRESIDENT
commidlist.append('C00494831') # FRIENDS OF BRIANNE MURPHY
commidlist.append('C00494849') # PERKINS FOR CONGRESS
commidlist.append('C00494856') # LOIS FRANKEL FOR CONGRESS
commidlist.append('C00494872') # LEVETIN FOR PRESIDENT
commidlist.append('C00494906') # DIANNE COSTA FOR US CONGRESS
commidlist.append('C00494914') # LISA WILSON-FOLEY FOR CONGRESS
commidlist.append('C00494922') # MIKE KOFFENBERGER FOR CONGRESS
commidlist.append('C00494963') # PAUL CHEHADE NATIONAL ELECTION COMMITTEE
commidlist.append('C00494989') # MIKE MUNZING FOR CONGRESS
commidlist.append('C00495051') # ELMER FUDD FOR GURLEY L MARTIN FOR PRESIDENT
commidlist.append('C00495069') # MADAME PRESIDENT TITTLE
commidlist.append('C00495093') # LYNNE TORGERSON FOR CONGRESS 2012, INC
commidlist.append('C00495119') # FRIENDS OF HEATHER MCTEER
commidlist.append('C00495127') # JEFFREY BAREA EXPLORATORY COMMITTEE
commidlist.append('C00495135') # NORMAN SOLOMON FOR CONGRESS COMMITTEE
commidlist.append('C00495168') # COMMITTEE TO ELECT TRACY DANIELS; THE
commidlist.append('C00495226') # CHUCK WILLIAMS FOR CONGRESS COMMITTEE
commidlist.append('C00495267') # FROST FOR CONGRESS
commidlist.append('C00495325') # CLARK FOR CONGRESS
commidlist.append('C00495416') # R W JENNA FOR CONGRESS
commidlist.append('C00495424') # JAMES SHINN FOR PRESIDENT PCC
commidlist.append('C00495432') # BROWN 2012
commidlist.append('C00495507') # MIKE BARKLEY FOR CONGRESS COMMITTEE
commidlist.append('C00495515') # LEWIS FOR CONGRESS
commidlist.append('C00495523') # ROB ZERBAN FOR CONGRESS
commidlist.append('C00495572') # SHEYMAN FOR CONGRESS
commidlist.append('C00495598') # CHRISTIE VILSACK FOR IOWA
commidlist.append('C00495606') # FRIENDS OF ROY MOORE
commidlist.append('C00495630') # SALMON FOR CONGRESS
commidlist.append('C00495721') # CITIZENTS FOR RAGHAVAN
commidlist.append('C00495739') # MARK B GRAHAM FOR PRESIDENT 2012
commidlist.append('C00495747') # FRIENDS OF JOHN REVELIS FOR PRESIDENT
commidlist.append('C00495770') # POLITICAL CAMPAIGN TO ELECT PHILLIP ANDREWS; THE
commidlist.append('C00495788') # RONALD DAVID JONES FOR PRESIDENT 2012
commidlist.append('C00495838') # JOANNE DOWDELL FOR CONGRESS
commidlist.append('C00495846') # ANN WAGNER FOR CONGRESS
commidlist.append('C00495853') # GRIEGO FOR CONGRESS
commidlist.append('C00495895') # HAROLD HEARD FOR PRESIDENT 2012
commidlist.append('C00495937') # ITAMAR GELBMAN FOR CONGRESS
commidlist.append('C00495945') # PAT GARCIA FOR CONGRESS
commidlist.append('C00495952') # SCHNEIDER FOR CONGRESS
commidlist.append('C00495978') # CASTLE FOR NEW JERSEY
commidlist.append('C00495986') # KIRK ADAMS FOR CONGRESS
commidlist.append('C00496026') # KREITLOW FOR CONGRESS
commidlist.append('C00496042') # COUTU FOR CONGRESS
commidlist.append('C00496059') # HECHT FOR CONGRESS
commidlist.append('C00496109') # PIRTLE FOR CONGRESS COMMITTEE
commidlist.append('C00496117') # KILGORE COMMITTEE
commidlist.append('C00496141') # JUN CHOI FOR CONGRESS INC
commidlist.append('C00496158') # NASCENZI FOR CONGRESS
commidlist.append('C00496190') # BOTHWELL FOR CONGRESS
commidlist.append('C00496208') # DAVE CROOKS FOR CONGRESS
commidlist.append('C00496216') # MCKENZIE FOR CONGRESS
commidlist.append('C00496273') # ED POTOSNAK FOR CONGRESS
commidlist.append('C00496299') # STRAW FOR CONGRESS
commidlist.append('C00496356') # MILLER FOR CONGRESS
commidlist.append('C00496364') # JOHN DOUGLASS FOR CONGRESS
commidlist.append('C00496430') # ELECT MARK CALLAHAN
commidlist.append('C00496455') # ROGER GARY PRESIDENTIAL CAMPAIGN COMMITTEE
commidlist.append('C00496471') # OCONNOR FOR CONGRESS
commidlist.append('C00496489') # BILL TOFTE FOR CONGRESS
commidlist.append('C00496513') # FRIENDS OF TARRYL CLARK 2012
commidlist.append('C00496554') # ROBERT LAUTEN FOR CONGRESS 2012
commidlist.append('C00496620') # DONOVAN FOR CONGRESS
commidlist.append('C00496646') # CAMPAIGN CLUB
commidlist.append('C00496687') # ANDRE BARNETT 2012 INC
commidlist.append('C00496695') # COMMITTEE TO ELECT WAYNE HARMON
commidlist.append('C00496778') # RAJA FOR CONGRESS
commidlist.append('C00496794') # TODD FOREMAN CONGRESS 2012
commidlist.append('C00496802') # FRIENDS OF JOHN ABARR
commidlist.append('C00496851') # DOHERTY FOR CONGRESS
commidlist.append('C00496869') # JOHN STACY FOR TEXAS
commidlist.append('C00496877') # ANDERS FOR CONGRESS
commidlist.append('C00496901') # MIKE BENNETT FOR CONGRESS
commidlist.append('C00496943') # HILL FOR AMERICA
commidlist.append('C00496950') # MIKE MOLONEY FOR PRESIDENT
commidlist.append('C00496968') # THOMAS J BRUZZESI FOR PRESIDENT INC
commidlist.append('C00497008') # VERL 4 PRESIDENT
commidlist.append('C00497016') # JOHNSON FOR CONGRESS 2012
commidlist.append('C00497024') # FRIENDS OF JOSEF VERNON HODGKINS FOR CONGRESS
commidlist.append('C00497040') # KALK FOR US HOUSE
commidlist.append('C00497065') # SAL PACE FOR CONGRESS
commidlist.append('C00497107') # PRATTAS FOR PRESIDENT
commidlist.append('C00497164') # EUGENE ROSELL HUNT JR
commidlist.append('C00497180') # COFFMAN FOR CONGRESS 2012
commidlist.append('C00497198') # MIKE WILLIAMS FOR CONGRESS
commidlist.append('C00497206') # COMMITTEE TO ELECT STEPHEN SHADDEN FOR PRESIDENT
commidlist.append('C00497214') # FRIENDS OF LAURA RUDERMAN
commidlist.append('C00497222') # SUSAN ADAMS FOR CONGRESS
commidlist.append('C00497230') # BOB EVANS 4 CONGRESS
commidlist.append('C00497255') # STAHL FOR CONGRESS
commidlist.append('C00497289') # POWELL FOR CONGRESS
commidlist.append('C00497321') # VARGAS FOR CONGRESS 2012
commidlist.append('C00497339') # TIMOTHY T DAY NEW GOP
commidlist.append('C00497354') # SOPHIA THE LOGOS
commidlist.append('C00497396') # TULSI FOR HAWAII
commidlist.append('C00497404') # WENONA FOR ARIZONA
commidlist.append('C00497479') # LANE FOR CONGRESS COMMITTEE
commidlist.append('C00497487') # FEAGLE FOR CONGRESS
commidlist.append('C00497495') # TRUE SONS OF LIBERTY
commidlist.append('C00497537') # KOEHLER FOR CONGRESS
commidlist.append('C00497552') # CAMPAIGN GRISKIE
commidlist.append('C00497628') # GRANTHAM FOR CONGRESS
commidlist.append('C00497636') # BYERLEY FOR PRESIDENT COMMITTEE 2012
commidlist.append('C00497644') # JIMMIE MOORE FOR CONGRESS
commidlist.append('C00497651') # KENNETH CORN EXPLORATORY COMMITTEE
commidlist.append('C00497735') # HARDCASTLE PRESIDENTIAL COMMITTEE
commidlist.append('C00497743') # BRIAN HOCKENSMITH FOR PRESIDENT CAMPAIGN FUND
commidlist.append('C00497750') # DAVE MONTGOMERY FOR PRESIDENT
commidlist.append('C00497768') # SEND TIM TO CONGRESS
commidlist.append('C00497776') # GILLAN FOR CONGRESS
commidlist.append('C00497784') # SAUERWEIN FOR CONGRESS
commidlist.append('C00497800') # DAVE STROHMAIER FOR CONGRESS
commidlist.append('C00497818') # WENSTRUP FOR CONGRESS
commidlist.append('C00497826') # FRIENDSOFCRAIGENNIS
commidlist.append('C00497834') # HYKES FOR THE AMERICAN DREAM
commidlist.append('C00497859') # HALL FOR CONGRESS EXPLORATORY COMMITTEE
commidlist.append('C00497867') # DALE BRUEGGEMANN FOR CONGRESS
commidlist.append('C00497875') # FARAH FOR THE PEOPLE
commidlist.append('C00497909') # HUNSICKER FOR CONGRESS
commidlist.append('C00497933') # CASTRO FOR CONGRESS
commidlist.append('C00497974') # ELIZABETH CHILDS FOR CONGRESS
commidlist.append('C00498030') # JEFF ANDERSON FOR MINNESOTA
commidlist.append('C00498048') # COMMITTEE TO KALIKO CASTILLE FOR CONGRESS
commidlist.append('C00498055') # JIM CRONE FOR CONGRESS
commidlist.append('C00498063') # JEFFREY HARRIS 2012
commidlist.append('C00498113') # PAUL SIMS FOR PRESIDENT
commidlist.append('C00498121') # ROGER WILLIAMS FOR U S CONGRESS COMMITTEE
commidlist.append('C00498139') # MICHAEL JOHNSON FOR CONGRESS INC
commidlist.append('C00498147') # DAVID ROBT FREY
commidlist.append('C00498162') # FRIENDS OF WALLACE
commidlist.append('C00498170') # COMMITTEE TO ELECT DAN SEBRING FOR CONGRESS
commidlist.append('C00498188') # JOHN TAVAGLIONE FOR CONGRESS
commidlist.append('C00498196') # KOSTER FOR CONGRESS - 2012
commidlist.append('C00498204') # FRIENDS OF JEFF MILLER FOR CONGRESS
commidlist.append('C00498212') # ALAN LOWENTHAL FOR CONGRESS
commidlist.append('C00498220') # MCCOTTER 2012
commidlist.append('C00498246') # FRANCIS J SAVARIRAYAN FOR PRESIDENT COMMITTEE
commidlist.append('C00498295') # HARRISON LEONARD FOR CONGRESS
commidlist.append('C00498303') # LINDSTROM FOR CONGRESS
commidlist.append('C00498311') # IMUS FOR CONGRESS
commidlist.append('C00498329') # COMMITTEE TO ELECT JOHN RUSSELL TO CONGRESS
commidlist.append('C00498337') # JOE MIKLOSI FOR CONGRESS
commidlist.append('C00498345') # MULLIN FOR CONGRESS
commidlist.append('C00498378') # DARSHAN RAUNIYAR FOR CONGRESS
commidlist.append('C00498394') # CAMPAIGN 2012 - ERIN MAGEE 1ST REPUBLICAN PRESIDENTIAL CANDIDATE FROM THE STATE OF FLORIDA
commidlist.append('C00498402') # ARCHER FOR CONGRESS
commidlist.append('C00498410') # ANDY SCHMOOKLER FOR CONGRESS
commidlist.append('C00498428') # KENT L WILLIAMS FOR PRESIDENT
commidlist.append('C00498451') # CITIZENS FOR PALOMO
commidlist.append('C00498469') # SUKHEE KANG FOR CONGRESS
commidlist.append('C00498493') # DAVE GARRISON FOR CONGRESS
commidlist.append('C00498501') # FRIENDS OF JUAN THOMAS
commidlist.append('C00498568') # FRIENDS OF CHERI BUSTOS
commidlist.append('C00498600') # SHAFFER FOR COLORADO
commidlist.append('C00498634') # DUCKWORTH FOR CONGRESS
commidlist.append('C00498642') # KEN GRAMMER FOR PRESIDENT INC
commidlist.append('C00498659') # PHILLIPS FOR PRESIDENT
commidlist.append('C00498667') # MARK TAKANO FOR CONGRESS
commidlist.append('C00498675') # NEW MEXICANS FOR MARTY CHAVEZ
commidlist.append('C00498683') # DAVID HERNANDEZ FOR CONGRESS 2012
commidlist.append('C00498766') # JOHN GREEN FERGUSON FOR PRESIDENT 2012
commidlist.append('C00498824') # TAMI STAINFIELD FOR PRESIDENT
commidlist.append('C00498840') # JOHN HATTER FOR CONGRESS
commidlist.append('C00498857') # HEATH WYNN FOR CONGRESS
commidlist.append('C00498873') # TONY CARDENAS FOR CONGRESS
commidlist.append('C00498881') # STINCHFIELD FOR CONGRESS
commidlist.append('C00498915') # JEFF BARTH CONGRESS
commidlist.append('C00498923') # VERMA FOR CONGRESS
commidlist.append('C00498964') # BURCH FOR CONGRESS
commidlist.append('C00498972') # FRIENDS OF DAVID GILL
commidlist.append('C00498980') # VAL DEMINGS FOR CONGRESS
commidlist.append('C00499012') # JANICE ARNOLD-JONES FOR CONGRESS
commidlist.append('C00499046') # RICH BECKER FOR CONGRESS
commidlist.append('C00499053') # NOLAN FOR CONGRESS VOLUNTEER COMMITTEE
commidlist.append('C00499061') # HOWARD STOPECK FOR CONGRESS
commidlist.append('C00499079') # STEVE RATHJE FOR CONGRESS
commidlist.append('C00499087') # CARL WIMMER FOR CONGRESS
commidlist.append('C00499111') # DALLAS CHAMBLESS FOR CONGRESS
commidlist.append('C00499129') # MITCHUM FOR CONGRESS
commidlist.append('C00499137') # SHARON SUND FOR CONGRESS
commidlist.append('C00499145') # HIRSCHBIEL FOR CONGRESS
commidlist.append('C00499152') # LUIS GARCIA FOR CONGRESS
commidlist.append('C00499160') # WES RIDDLE FOR US CONGRESS
commidlist.append('C00499178') # JEFF SEMON COMMITTEE TO ELECT FOR US CONGRESS
commidlist.append('C00499194') # COMMITTEE TO ELECT LEAH LAX
commidlist.append('C00499236') # GEORGE HOLDING FOR CONGRESS
commidlist.append('C00499277') # FRIENDS OF ERIC REYES
commidlist.append('C00499368') # LEE ROGERS FOR CONGRESS
commidlist.append('C00499392') # VALADAO FOR CONGRESS
commidlist.append('C00499426') # VINSKO FOR CONGRESS
commidlist.append('C00499459') # ENGSTRAND FOR CONGRESS DIST 36-TX
commidlist.append('C00499467') # TITUS FOR CONGRESS
commidlist.append('C00499483') # CITIZENS WITH TOM GUARENTE
commidlist.append('C00499491') # ANDREW HUGHES FOR CONGRESS
commidlist.append('C00499509') # FRIENDS OF COBBY M WILLIAMS
commidlist.append('C00499541') # PAUL COBLE FOR CONGRESS
commidlist.append('C00499558') # JOHN W EWING JR FOR U.S. CONGRESS
commidlist.append('C00499566') # TIM DAY FOR US CONGRESS
commidlist.append('C00499574') # FRIENDS OF JOE DAVIDOW
commidlist.append('C00499582') # KAREN KWIATKOWSKI FOR CONGRESS
commidlist.append('C00499590') # MICHAEL TRUNCALE FOR CONGRESS
commidlist.append('C00499608') # GEORGE FAUGHT FOR CONGRESS
commidlist.append('C00499681') # NO NEED TO DELVE: HOFF FOR PRESIDENT IN TWELVE
commidlist.append('C00499707') # COMMITTEE TO ELECT DAN DOLAN
commidlist.append('C00499715') # ROBINSON FOR CONGRESS.COM
commidlist.append('C00499723') # DAVID JON SPONHEIM FOR PRESIDENT
commidlist.append('C00499749') # JOE CHOW FOR U.S. CONGRESS
commidlist.append('C00499756') # NORMA MACIAS FOR CONGRESS
commidlist.append('C00499772') # JOHN WEBB 2012
commidlist.append('C00499806') # HECTOR FERRER COMISIONADO 2012
commidlist.append('C00499814') # MULLEN FOR CONGRESS
commidlist.append('C00499822') # ALYSON HUBER CONGRESSIONAL EXPLORATORY COMMITTEE
commidlist.append('C00499830') # AARON LEON AMMANN FOR PRESIDENT
commidlist.append('C00499848') # POLLOCK FOR CONGRESS
commidlist.append('C00499855') # COMMITTEE TO ELECT MAX RIEKSE
commidlist.append('C00499897') # MARKO LIIAS FOR CONGRESS
commidlist.append('C00499905') # BRIAN MATTHEWS FOR CONGRESS
commidlist.append('C00499947') # FRIENDS OF DAN KILDEE
commidlist.append('C00499954') # KEADLE FOR CONGRESS 2012
commidlist.append('C00499962') # OCEGUERA FOR CONGRESS
commidlist.append('C00499970') # WRITE-IN-REED
commidlist.append('C00499988') # COTTON FOR CONGRESS
commidlist.append('C00500041') # GATES4IOWA
commidlist.append('C00500058') # FRIENDS OF DAVID FOR CONGRESS
commidlist.append('C00500066') # DUSTIN ROWE FOR CONGRESS
commidlist.append('C00500074') # FRIENDS OF GARY DELONG
commidlist.append('C00500082') # SILVIA STAGG FOR PRESIDENT CAMPAIGN COMMITTEE
commidlist.append('C00500108') # TIFFANY RENEE FOR CONGRESS
commidlist.append('C00500132') # GLEAN CAMPAIGN COMMITTEE
commidlist.append('C00500140') # TONYLONGFORCONGRESS
commidlist.append('C00500157') # SOLUTIONS OR INSOLVENCY
commidlist.append('C00500165') # WILKES FOR CONGRESS
commidlist.append('C00500173') # DAVID MCINTOSH FOR INDIANA
commidlist.append('C00500181') # ANTHONY PROWELL FOR CONGRESS
commidlist.append('C00500199') # WILLIAMSON FOR U S CONGRESS
commidlist.append('C00500207') # FRIENDS OF SUSAN BROOKS
commidlist.append('C00500231') # DOC ADAMS FOR PRESIDENT
commidlist.append('C00500272') # SPENCE CAMPBELL FOR CONGRESS
commidlist.append('C00500280') # HOSMER FOR CONGRESS
commidlist.append('C00500314') # HARRY BRAUN FOR PRESIDENT
commidlist.append('C00500322') # JERRY LANSER FOR PRESIDENT
commidlist.append('C00500397') # FRIENDS OF JIM NEIDNER FOR CONGRESS
commidlist.append('C00500439') # STEVE HOBBS FOR CONGRESS
commidlist.append('C00500462') # STACEY LAWSON FOR CONGRESS
commidlist.append('C00500470') # KIAAINA FOR CONGRESS
commidlist.append('C00500488') # RON CALDERON FOR CONGRESS
commidlist.append('C00500496') # DR. PAM BARLOW FOR CONGRESS COMMITTEE
commidlist.append('C00500504') # LORI SALDANA FOR CONGRESS
commidlist.append('C00500553') # GEORGE DEMOS FOR CONGRESS 2012
commidlist.append('C00500595') # STEVE MOATS FOR 2012
commidlist.append('C00500611') # FRIENDS OF DAKOTA WOOD
commidlist.append('C00500629') # VOTE KARLA ROMERO
commidlist.append('C00500645') # KHIZAR JAFRI FOR CONGRESS
commidlist.append('C00500652') # COMMITTEE TO ELECT CHRIS PEDERSEN, THE
commidlist.append('C00500660') # HARPER FOR CONGRESS
commidlist.append('C00500678') # RUBIO FOR CONGRESS 2012
commidlist.append('C00500686') # MARK SHARPE FOR CONGRESS
commidlist.append('C00500694') # FRIENDS OF CATHY JOHNSON PENDLETON
commidlist.append('C00500710') # BARRY FOR CONGRESS
commidlist.append('C00500728') # JEFF HUNT FOR CONGRESS
commidlist.append('C00500751') # R BENEDICT MAYERS FOR PRESIDENT COMMITTEE
commidlist.append('C00500801') # RICETOWN ROYAL REPUBLIC
commidlist.append('C00500827') # JOHN LEE FOR CONGRESS
commidlist.append('C00500876') # RICHARD REED FOR PRESIDENT CAMPAIGN COMMITTEE
commidlist.append('C00500892') # KEN FORTENBERRY FOR US CONGRESS
commidlist.append('C00500900') # KIM DOLBOW VANN FOR CONGRESS
commidlist.append('C00500918') # CHRIS FIELDS FOR CONGRESS
commidlist.append('C00500926') # ANTENORI CONGRESSIONAL EXPLORATORY COMMITTEE
commidlist.append('C00500942') # KRISTI RISK FOR CONGRESS
commidlist.append('C00500959') # FRIENDS OF CHERILYN EAGAR
commidlist.append('C00500967') # SIMS FOR CONGRESS
commidlist.append('C00500975') # TETALMAN FOR CONGRESS
commidlist.append('C00500983') # JUSTIN WINTERS FOR CONGRESS
commidlist.append('C00500991') # TIMOTHY MURPHY FOR CONGRESS
commidlist.append('C00501049') # KUYKENDALL CONGRESSIONAL COMMITTEE
commidlist.append('C00501056') # JIM HICKEY FOR CONGRESS
commidlist.append('C00501064') # GEORGE RHODES FOR PRESIDENT
commidlist.append('C00501072') # DEAN YOUNG FOR CONGRESS COMMITTEE
commidlist.append('C00501080') # BUSTAMANTE FOR CONGRESS
commidlist.append('C00501122') # PILLICH FOR CONGRESS
commidlist.append('C00501155') # CHAD WILBANKS FOR CONGRESS
commidlist.append('C00501197') # BETO O'ROURKE FOR CONGRESS
commidlist.append('C00501205') # JOE KAUFMAN FOR CONGRESS
commidlist.append('C00501213') # CHARLES SCHAUPP FOR CONGRESS 2012
commidlist.append('C00501221') # BILL MCCUNE DEMOCRAT FOR U.S. CONGRESS
commidlist.append('C00501254') # COMMITTEE TO ELECT MICHELLE LUJAN GRISHAM
commidlist.append('C00501296') # DWAYNE THOMPSON US CONGRESS 2012
commidlist.append('C00501312') # JOE KOPSICK FOR CONGRESS
commidlist.append('C00501320') # MATTSNYDERFORPRESIDENT.COM
commidlist.append('C00501338') # CITIZENS TO ELECT FREDERICK COLLINS
commidlist.append('C00501346') # WILDMAN FOR PRESIDENT COMMITTEE
commidlist.append('C00501395') # FRIENDS OF MIKE BOLAND
commidlist.append('C00501403') # GARY STEPHENS US CONGRESS CAMPAIGN
commidlist.append('C00501411') # BRAD BOOKOUT FOR CONGRESS
commidlist.append('C00501551') # RALPH PRUYN FOR CONGRESS
commidlist.append('C00501569') # HANSEN FOR AMERICA
commidlist.append('C00501577') # RJ HARRIS 2012
commidlist.append('C00501585') # FRIENDS OF MIKE JACKSON CAMPAIGN
commidlist.append('C00501593') # CODY ROBERT JUDY FOR PRESIDENT 2012 U S C ELIGIBILITY CAMPAIGN
commidlist.append('C00501601') # JASON BUCK FOR CONGRESS
commidlist.append('C00501635') # PALOMBO FOR CONGRESS COMMITTEE
commidlist.append('C00501643') # DAVID ROUZER FOR CONGRESS
commidlist.append('C00501684') # JEFF BLOCK PRESIDENT FOR 100 DAYS INC
commidlist.append('C00501692') # VIVEK BAVDA FOR CONGRESS
commidlist.append('C00501700') # COMMITTEE TO ELECT ANDY CAFFREY TO CONGRESS
commidlist.append('C00501718') # COMMITTEE TO ELECT RICH EVANS
commidlist.append('C00501726') # ROBERT JORDAN FOR PRESIDENT
commidlist.append('C00501734') # LANCE ENDERLE FOR CONGRESS
commidlist.append('C00501809') # GREG AGUILAR FOR CONGRESS
commidlist.append('C00501817') # STUTZ FOR CONGRESS
commidlist.append('C00501833') # HANNEMANN FOR CONGRESS
commidlist.append('C00501841') # JACK HEIDEL FOR CONGRESS
commidlist.append('C00501874') # MICHAEL SLOAN FOR PRESIDENT
commidlist.append('C00501882') # MEALER 2012
commidlist.append('C00501890') # HOFFMAN FOR CONGRESS
commidlist.append('C00501908') # FRIENDS OF PETE GALLEGO
commidlist.append('C00501924') # BARBARA MALLORY CARAWAY FOR CONGRESS
commidlist.append('C00501957') # GONZALEZ FOR CONGRESS COMMITTEE
commidlist.append('C00501965') # KELDA FOR CONGRESS
commidlist.append('C00501973') # MARTHA FOR CONGRESS
commidlist.append('C00501981') # ELMO M AYCOCK FOR CONGRESS 2012
commidlist.append('C00502005') # DRUMMOND 2012
commidlist.append('C00502013') # RAKOWITZ FOR PRESIDENT
commidlist.append('C00502039') # COLLINS FOR CONGRESS
commidlist.append('C00502047') # SHURIN FOR CONGRESS
commidlist.append('C00502054') # SCHERER FOR CONGRESS
commidlist.append('C00502062') # JOSE PEIXOTO FOR US CONGRESS
commidlist.append('C00502070') # WAYNE IVERSON FOR CONGRESS
commidlist.append('C00502088') # CORBETT FOR CONGRESS
commidlist.append('C00502104') # DAN BOLLING FOR CONGRESS
commidlist.append('C00502138') # KENNETH WADE ADEN 4 CONGRESS
commidlist.append('C00502146') # JIM REED FOR CONGRESS
commidlist.append('C00502161') # BRITTON FOR CONGRESS
commidlist.append('C00502179') # MARK POCAN FOR CONGRESS
commidlist.append('C00502203') # DENISE MORENO DUCHENY FOR CONGRESS
commidlist.append('C00502229') # WEBER FOR CONGRESS
commidlist.append('C00502237') # COURTNEY FOR CONGRESS 2012
commidlist.append('C00502245') # WAYNE HERRIMAN FOR CONGRESS
commidlist.append('C00502294') # SWALWELL FOR CONGRESS
commidlist.append('C00502302') # ANDERSON FOR CONGRESS
commidlist.append('C00502310') # FELICIA HARRIS FOR CONGRESS
commidlist.append('C00502328') # MARCUS RICHMOND FOR CONGRESS
commidlist.append('C00502336') # TROY EDGAR FOR CONGRESS
commidlist.append('C00502385') # WIFORD FOR AMERICA 2012
commidlist.append('C00502393') # FRIENDS OF JIM BRIDENSTINE
commidlist.append('C00502443') # WILL MOORE FOR CONGRESS 2012
commidlist.append('C00502484') # KLAUDER4CONGRESS
commidlist.append('C00502492') # ARGENZIANO FOR CONGRESS
commidlist.append('C00502500') # FRIENDS OF WAYNE PETTIGREW
commidlist.append('C00502534') # GLORIA NEGRETE MCLEOD FOR CONGRESS
commidlist.append('C00502575') # DR. RAUL RUIZ FOR CONGRESS 2012 COMMITTEE
commidlist.append('C00502583') # JOHN MCDONALD FOR CONGRESS
commidlist.append('C00502609') # FRIENDS OF PETE RIEHM
commidlist.append('C00502617') # WORZALA FOR CONGRESS
commidlist.append('C00502666') # YOUNTS FOR CONGRESS COMMITTEE
commidlist.append('C00502674') # YARBER FOR MISSOURI
commidlist.append('C00502682') # WAYNE WINSLEY FOR CONGRESS
commidlist.append('C00502690') # JACKIE GOUGE FOR PRESIDENT
commidlist.append('C00502716') # BOB MARX FOR HAWAII
commidlist.append('C00502724') # RCJPAC
commidlist.append('C00502773') # RUBEN KIHUEN FOR CONGRESS
commidlist.append('C00502781') # DANIEL ROBERTS FOR CONGRESS
commidlist.append('C00502831') # JUSTIN HEWLETT FOR CONGRESS
commidlist.append('C00502864') # COMMITTEE TO ELECT WILLIAM A FAULK JR FOR CONGRESS
commidlist.append('C00502872') # THADVIERS.COM
commidlist.append('C00502922') # TURNER FOR PRESIDENT
commidlist.append('C00502989') # JOSE HERNANDEZ FOR CONGRESS
commidlist.append('C00502997') # DE LA PAZ FOR CONGRESS
commidlist.append('C00503011') # COMMITTEE TO ELECT MITCH FEIKES 2012
commidlist.append('C00503029') # COMMITTEE TO ELECT AURORA LOPEZ FOR PRESIDENT
commidlist.append('C00503037') # MICHAEL WHITLEY FOR PRESIDENT
commidlist.append('C00503045') # STEPHEN SANDSTROM FOR CONGRESS
commidlist.append('C00503052') # JEFFRIES FOR CONGRESS
commidlist.append('C00503094') # MEADOWS FOR CONGRESS
commidlist.append('C00503102') # EVAN FEINBERG FOR CONGRESS
commidlist.append('C00503110') # SCOTT PETERS FOR CONGRESS
commidlist.append('C00503128') # SCATES FOR CONGRESS
commidlist.append('C00503169') # TAJ FOR CONGRESS
commidlist.append('C00503177') # BETTE GRANDE FOR CONGRESS
commidlist.append('C00503185') # RO FOR CONGRESS INC
commidlist.append('C00503243') # BAILEY FOR CONGRESS
commidlist.append('C00503276') # SLEZAK FOR CONGRESS
commidlist.append('C00503284') # PAM GULLESON FOR NORTH DAKOTA
commidlist.append('C00503292') # LARRYYOUNGBLOOD4CONGRESS
commidlist.append('C00503334') # RICK TUBBS FOR CONGRESS
commidlist.append('C00503342') # TOM ENGEL FOR CONGRESS
commidlist.append('C00503359') # MARK OXNER FOR CONGRESS
commidlist.append('C00503383') # OZZIE FOR CONGRESS
commidlist.append('C00503433') # JOE FOR CONGRESS 2012
commidlist.append('C00503466') # COMMITTEE TO ELECT ANNA M TRUJILLO TO CONGRESS; THE
commidlist.append('C00503474') # JOTTE FOR CONGRESS
commidlist.append('C00503482') # DEMEO FOR CONGRESS
commidlist.append('C00503490') # BANAFSHEH AKHLAGHI FOR CONGRESS
commidlist.append('C00503508') # PETZEL FOR CONGRESS
commidlist.append('C00503516') # RESKE FOR CONGRESS
commidlist.append('C00503524') # FARRIS FOR CONGRESS
commidlist.append('C00503532') # KELCEY WILSON FOR PRESIDENT
commidlist.append('C00503565') # WESTON WAMP FOR CONGRESS
commidlist.append('C00503631') # RUSCITTI FOR CONGRESS
commidlist.append('C00503649') # HOOSER FOR HAWAII
commidlist.append('C00503656') # COMMITTEE TO ELECT JACK ARNOLD
commidlist.append('C00503664') # FRIENDS OFCHRIS SCILEPPI
commidlist.append('C00503672') # CITIZENS FOR RAY LODATO
commidlist.append('C00503698') # FRIENDS OF MIKE KOWALL FOR CONGRESS
commidlist.append('C00503706') # PARRY FOR CONGRESS
commidlist.append('C00503714') # MEEK FOR CONGRESS
commidlist.append('C00503722') # VINCE SAWYER FOR CONGRESS
commidlist.append('C00503730') # COMMITTEE TO ELECT EVELYN MADRID ERHARD
commidlist.append('C00503748') # JAY OLD FOR CONGRESS
commidlist.append('C00503755') # GAIL DIGNAM FOR CONGRESS EXPLORATORY COMMITTEE
commidlist.append('C00503763') # COMMITTEE TO ELECT KARIN L SWANSON FOR PRESIDENT
commidlist.append('C00503771') # AVERAGE JOE FOR PRESIDENT JOE STORY, THE
commidlist.append('C00503797') # DECKER FOR CONGRESS
commidlist.append('C00503854') # WALL FOR CONGRESS
commidlist.append('C00503862') # COMMITTEE TO ELECT LAURA MOLINA
commidlist.append('C00503896') # VONDERSAAR FOR CONGRESS
commidlist.append('C00503912') # KATHYERN LANE FOR THE PEOPLES PRESIDENT
commidlist.append('C00503920') # GARAGIOLA FOR CONGRESS
commidlist.append('C00503946') # KOVACH FOR CONGRESS INC
commidlist.append('C00503953') # WICKMAN FOR CONGRESS
commidlist.append('C00503995') # FRIENDS OF MATT ALEXANDER
commidlist.append('C00504001') # CAMPAIGN TO ELECT ALOYS RUTAGWIBIRA FOR CONGRESS
commidlist.append('C00504019') # RICK W ALLEN FOR CONGRESS
commidlist.append('C00504027') # YARBROUGH FOR LIBERTY
commidlist.append('C00504035') # KERRY BENTIVOLIO FOR US CONGRESS
commidlist.append('C00504068') # BARNES FOR CONGRESS
commidlist.append('C00504076') # DANIEL FANNING FOR CONGRESS
commidlist.append('C00504092') # YALE FOR CONGRESS
commidlist.append('C00504100') # WADE BROWN 2012
commidlist.append('C00504118') # ROASEAU FOR PRESIDENT
commidlist.append('C00504167') # ALBERT MORZUCH 2012
commidlist.append('C00504175') # FRIENDS OF STEPHEN K SIMPSON INC
commidlist.append('C00504217') # COMMITTEE TO ELECT ANGELA VALLES TO CONGRESSIONAL 8TH DISTRICT
commidlist.append('C00504225') # DON JAQUESS FOR CONGRESS
commidlist.append('C00504258') # FRIENDS OF ALEX BORGOGNONE
commidlist.append('C00504282') # KRAUS 4 CONGRESS
commidlist.append('C00504290') # ROB WALLACE FOR CONGRESS 2012
commidlist.append('C00504324') # COMMITTEE TO ELECT JAMES F HANING II
commidlist.append('C00504332') # SUSAN NARVAIZ FOR CONGRESS
commidlist.append('C00504340') # PLUMMER FOR CONGRESS
commidlist.append('C00504357') # STEVE OBSITNIK FOR CONGRESS, INC
commidlist.append('C00504381') # ORNER FOR CONGRESS
commidlist.append('C00504399') # CITIZENS TO ELECT SUE THORN CONGRESS 2012
commidlist.append('C00504407') # JOHN D FOR CONGRESS
commidlist.append('C00504415') # GODFREY DILLARD FOR CONGRESS
commidlist.append('C00504423') # COMMITTEE TO ELECT TED WAGA III
commidlist.append('C00504431') # JOHN WHITLEY FOR CONGRESS
commidlist.append('C00504449') # KENNETH GODWIN FOR PREZ
commidlist.append('C00504456') # MARK STEVENS FOR PRESIDENT
commidlist.append('C00504480') # COMMITTEE TO ELECT JOYCE B SEGERS FOR CONGRESS
commidlist.append('C00504498') # ROSE MEZA HARRISON FOR CONGRESS
commidlist.append('C00504522') # HUDSON FOR CONGRESS
commidlist.append('C00504548') # LARRY SMITH FOR CONGRESS
commidlist.append('C00504589') # ALEX MARTINEZ 2012 LLC
commidlist.append('C00504597') # TROIANI2012
commidlist.append('C00504613') # HORSFORD FOR CONGRESS
commidlist.append('C00504621') # FRIENDS OF LOIS MYERS CAMPAIGN
commidlist.append('C00504670') # GWEN HOWARD FOR CONGRESS
commidlist.append('C00504688') # OTERO FOR CONGRESS
commidlist.append('C00504704') # CRAMER FOR CONGRESS
commidlist.append('C00504712') # STILL 2012
commidlist.append('C00504720') # TAMMY HALL FOR CONGRESS
commidlist.append('C00504795') # COMMITTEE TO ELECT DAN GRANT
commidlist.append('C00504803') # DAVID GUNTER FOR CONGRESS
commidlist.append('C00504811') # BARBARA CARRASCO FOR CONGRESS COMMITTEE
commidlist.append('C00504829') # SANCHEZ FOR CONGRESS
commidlist.append('C00504837') # BERT JOHNSON FOR U. S. CONGRESS
commidlist.append('C00504845') # ELECT CLARK HALL
commidlist.append('C00504852') # PERRY HANEY FOR CONGRESS EXPLORATORY COMMITTEE
commidlist.append('C00504878') # HOWARDKNEPPER PERSIDENTIAL CAMPAIGN
commidlist.append('C00504886') # FRIENDS OF MIKE STEINBERG INC
commidlist.append('C00504894') # GENE JEFFRESS FOR CONGRESS
commidlist.append('C00504902') # HAYWOOD FOR PRESIDENT
commidlist.append('C00504936') # FRIENDS OF DAN SCHWARTZ
commidlist.append('C00504944') # MATT SILVERMAN FOR CONGRESS
commidlist.append('C00504951') # JACOBSEN FOR CONGRESS
commidlist.append('C00504977') # DAWN HOWARD FOR OHIO
commidlist.append('C00504985') # RORABACK FOR CONGRESS
commidlist.append('C00504993') # ANDRE BAUER FOR CONGRESS
commidlist.append('C00505008') # JASON STERLING FOR FREEDON
commidlist.append('C00505016') # CITIZENS FOR COOK
commidlist.append('C00505024') # JOE GOLDNER FOR CONGRESS 2012
commidlist.append('C00505040') # TIMMY STRICKLAND FOR PRESIDENT
commidlist.append('C00505065') # GLENN IVEY FOR CONGRESS
commidlist.append('C00505073') # CITIZENS FOR THERESA KORMOS
commidlist.append('C00505123') # GLENN ANDERSON FOR CONGRESS
commidlist.append('C00505131') # ALVIN PETERS FOR CONGRESS
commidlist.append('C00505156') # MILAD FOR CONGRESS
commidlist.append('C00505164') # MORGAN FOR CONGRESS
commidlist.append('C00505172') # MONTOYA FOR CONGRESS
commidlist.append('C00505198') # AUBUCHON FOR CONGRESS
commidlist.append('C00505255') # WRIGHT MCLEOD FOR CONGRESS
commidlist.append('C00505263') # STEWART ALEXANDER FOR PRESIDENT CAMPAIGN COMMITTEE
commidlist.append('C00505271') # COMMITTEE FOR MICHAEL LERMAN
commidlist.append('C00505339') # TODD RICHARD GLORE FOR PRESIDENT
commidlist.append('C00505347') # DR TERRY JONES 2012
commidlist.append('C00505362') # RYAN MCEACHRON FOR CONGRESS
commidlist.append('C00505370') # FRIENDS OF CHAUNCEY GOSS
commidlist.append('C00505388') # CHRIS MILLER FOR CONGRESS
commidlist.append('C00505396') # DUCHY TRACHTENBERG FOR CONGRESS
commidlist.append('C00505404') # CHRISTOPHER DAVID FOR CONGRESS
commidlist.append('C00505412') # DARCY BURNER FOR CONGRESS
commidlist.append('C00505420') # COMMITTEE FOR DANIEL J BEJGER PRESIDENT OF THE UNITED STATES
commidlist.append('C00505438') # OPITZ FOR CONGRESS
commidlist.append('C00505446') # TOMOTHY C WOLFE FOR CONGRESS
commidlist.append('C00505453') # CECIL JAMES ROTH FOR PRESIDENT
commidlist.append('C00505461') # JOEL PHELPS FOR CONGRESS
commidlist.append('C00505479') # ALAN WOODRUFF FOR CONGRESS
commidlist.append('C00505487') # FRIENDS OF PARNELL DIGGS
commidlist.append('C00505529') # JUSTIN STERNAD FOR CONGRESS
commidlist.append('C00505537') # SCALA FOR CONGRESS
commidlist.append('C00505560') # CLYDE WILLIAMS FOR CONGRESS EXPLORATORY COMMITTEE
commidlist.append('C00505586') # CHARLES W BRADLEY
commidlist.append('C00508200') # 1911 UNITED
commidlist.append('C00502633') # 50 STATE STRATEGY
commidlist.append('C00504241') # 9-9-9 FUND
commidlist.append('C00505305') # A PROMISE TO OUR CHILDREN
commidlist.append('C00504779') # ABO 2012 SUPER PAC INC
commidlist.append('C00505792') # ACU SUPER PAC
commidlist.append('C00456624') # AIG INSURANCE CUSTOMERS SUPER PAC
commidlist.append('C00456012') # ALASKA NATIVES TRIBE SUPER PAC
commidlist.append('C00457465') # ALLSTATE INSURANCE CUSTOMERS SUPER PAC
commidlist.append('C00507541') # AMERICA'S SUPER ALLIANCE POLITICAL ACTION COMMITTEE
commidlist.append('C00456111') # AMERICAN AIRLINES CUSTOMERS SUPER PAC
commidlist.append('C00507566') # AMERICAN CROSSWINDS PAC
commidlist.append('C00457481') # AMERICAN INDIANS TRIBE SUPER PAC
commidlist.append('C00503839') # AMERICAN PHOENIX SUPERPAC
commidlist.append('C00456160') # AMERICAN RED CROSS RELIEF FUND SUPER PAC
commidlist.append('C00507244') # AMERICANLP
commidlist.append('C00507046') # AMERICANS FOR A BETTER TOMORROW TODAY
commidlist.append('C00456616') # AMTRUST BANK CUSTOMERS SUPER PAC
commidlist.append('C00507533') # ARTICLEIISUPERPAC
commidlist.append('C00456434') # BANK OF AMERICA CUSTOMERS SUPER PAC
commidlist.append('C00456343') # BLOOMINGDALE'S DEPARTMENT STORE CUSTOMERS SUPER PAC
commidlist.append('C00503557') # BRADY BUNCH PAC
commidlist.append('C00507707') # CAIN CONNECTIONS PAC
commidlist.append('C00456376') # CHASE BANK CUSTOMERS SUPER PAC
commidlist.append('C00456095') # CITIBANK CUSTOMERS SUPER PAC
commidlist.append('C00491811') # CITIZENS ALLIANCE FOR BETTER CANDIDATES
commidlist.append('C00506113') # COALITION FOR AMERICAN VALUES PAC
commidlist.append('C00490920') # COMMITTEE FOR A NEW START IN THE RIGHT DIRECTION
commidlist.append('C00507228') # COMMITTEE TO ELECT AN EFFECTIVE VALLEY CONGRESSMAN
commidlist.append('C00504530') # CONGRESSIONAL LEADERSHIP FUND
commidlist.append('C00456517') # COSTCO STORE CUSTOMERS SUPER PAC
commidlist.append('C00507517') # CREDO SUPERPAC
commidlist.append('C00456178') # DEMOCRATIC CONGRESSIONAL / SENATORIAL AND PRESIDENTIAL CAMPAIGNS FUND COMMITTEE
commidlist.append('C00503789') # DGA ACTION
commidlist.append('C00502880') # ECONOMIC INNOVATION ACTION FUND
commidlist.append('C00508002') # ENDORSE LIBERTY INC
commidlist.append('C00456442') # FEDERAL RESERVE BANK EMPLOYEES SUPER PAC
commidlist.append('C00506808') # FEEL THE HEAT PAC INC
commidlist.append('C00457531') # FIDELITY INVESTMENTS CUSTOMERS SUPER PAC
commidlist.append('C00456400') # GENERAL MOTORS CUSTOMERS SUPER PAC
commidlist.append('C00493510') # GLOBAL DIASPORA PAC INCORPORATED; THE
commidlist.append('C00456210') # GOLDMAN SACHS GROUP CUSTOMERS SUPER PAC
commidlist.append('C00456608') # HARVARD UNIVERSITY GRADUATES SUPER PAC
commidlist.append('C00456046') # HILTON HOTEL CUSTOMERS SUPER PAC
commidlist.append('C00508440') # HUMAN RIGHTS CAMPAIGN EQUALITY VOTES
commidlist.append('C00503540') # JAN PAC
commidlist.append('C00456285') # JC PENNEY DEPARTMENT STORE CUSTOMERS SUPER PAC
commidlist.append('C00503458') # LA FORWARD INC
commidlist.append('C00508317') # LEADERS FOR FAMILIES SUPER PAC INC
commidlist.append('C00457515') # MACY'S DEPARTMENT STORE CUSTOMERS SUPER PAC
commidlist.append('C00456053') # MARRIOTT HOTEL CUSTOMERS SUPER PAC
commidlist.append('C00505701') # NATIONAL REPUBLICAN WOMEN'S COMMITTEE
commidlist.append('C00456590') # NATIVE AMERICANS TRIBE SUPER PAC
commidlist.append('C00503193') # PARENTS FOR A BRIGHTER FUTURE
commidlist.append('C00492595') # PROGRESSIVE KICK INDEPENDENT EXPENDITURES
commidlist.append('C00507053') # PURO PAC
commidlist.append('C00508150') # REAL LEADER PAC
commidlist.append('C00503417') # RED WHITE AND BLUE FUND
commidlist.append('C00456236') # REGIONS BANK CUSTOMERS SUPER PAC
commidlist.append('C00503573') # RENEW DELAWARE PAC
commidlist.append('C00456061') # REPUBLICAN CONGRESSIONAL / SENATORIAL AND PRESIDENTIAL CAMPAIGNS FUND COMMITTEE
commidlist.append('C00506972') # REPUBLICAN TRUTH SQUAD PAC
commidlist.append('C00507509') # RESTART CONGRESS POLITICAL ACTION COMMITTEE
commidlist.append('C00456152') # RESTORE OUR ECONOMY SUPER PAC
commidlist.append('C00506816') # RESTORE TRUST PAC INC
commidlist.append('C00507921') # RON PAUL VOLUNTEERS PAC
commidlist.append('C00457473') # SEARS DEPARTMENT STORE CUSTOMERS SUPER PAC
commidlist.append('C00457457') # SOCIAL SECURITY ADMINISTRATION EMPLOYEES SUPER PAC
commidlist.append('C00505719') # SOLUTIONS 2012
commidlist.append('C00506543') # SPIRIT OF AMERICA SOLUTIONS
commidlist.append('C00457499') # STATE FARM INSURANCE CUSTOMERS SUPER PAC
commidlist.append('C00505081') # STRONG AMERICA NOW SUPER PAC
commidlist.append('C00456186') # SUNTRUST BANK CUSTOMERS SUPER PAC
commidlist.append('C00504464') # TEA PAC
commidlist.append('C00506469') # TEA PARTY FUND
commidlist.append('C00505180') # TEXAS AGGIES FOR PERRY 2012
commidlist.append('C00456103') # UNITED STATES BILLIONAIRES SUPER PAC
commidlist.append('C00456194') # UNITED STATES CONGRESSMEN SUPER PAC
commidlist.append('C00457507') # UNITED STATES DEPARTMENT OF AGRICULTURE EMPLOYEES SUPER PAC
commidlist.append('C00456038') # UNITED STATES DEPARTMENT OF COMMERCE EMPLOYEES SUPER PAC
commidlist.append('C00456582') # UNITED STATES DEPARTMENT OF DEFENSE EMPLOYEES SUPER PAC
commidlist.append('C00456533') # UNITED STATES DEPARTMENT OF EDUCATION EMPLOYEES SUPER PAC
commidlist.append('C00456079') # UNITED STATES DEPARTMENT OF ENERGY EMPLOYEES SUPER PAC
commidlist.append('C00456657') # UNITED STATES DEPARTMENT OF HEALTH EMPLOYEES SUPER PAC
commidlist.append('C00457549') # UNITED STATES DEPARTMENT OF HOUSING AND URBAN DEVELOPMENT EMPLOYEES SUPER PAC
commidlist.append('C00456491') # UNITED STATES DEPARTMENT OF HOMELAND SECURITY EMPLOYEES SUPER PAC
commidlist.append('C00456541') # UNITED STATES DEPARTMENT OF JUSTICE EMPLOYEES SUPER PAC
commidlist.append('C00456640') # UNITED STATES DEPARTMENT OF LABOR EMPLOYEES SUPER PAC
commidlist.append('C00456426') # UNITED STATES DEPARTMENT OF STATE EMPLOYEES SUPER PAC
commidlist.append('C00456475') # UNITED STATES DEPARTMENT OF THE TREASURY EMPLOYEES SUPER PAC
commidlist.append('C00456459') # UNITED STATES DEPARTMENT OF THE INTERIOR EMPLOYEES SUPER PAC
commidlist.append('C00456566') # UNITED STATES DEPARTMENT OF TRANSPORTATION EMPLOYEES SUPER PAC
commidlist.append('C00456087') # UNITED STATES FILM STARS SUPER PAC
commidlist.append('C00456483') # UNITED STATES MULTI-MILLIONAIRES SUPER PAC
commidlist.append('C00456202') # UNITED STATES MUSIC STARS SUPER PAC
commidlist.append('C00456749') # UNITED STATES SENATORS SUPER PAC
commidlist.append('C00456368') # UNITED STATES SPORT PLAYERS SUPER PAC
commidlist.append('C00456756') # UNITED STATES SUPREME COURT EMPLOYEES SUPER PAC
commidlist.append('C00456392') # UNITED WAY MONEY DONORS SUPER PAC
commidlist.append('C00456020') # USAID EMPLOYEES SUPER PAC
commidlist.append('C00456574') # USCIS EMPLOYEES SUPER PAC
commidlist.append('C00505321') # VALLEY-ISRAEL ALLIANCE
commidlist.append('C00503367') # VOTERS FOR COMMON SENSE
commidlist.append('C00456384') # WAL-MART STORES CUSTOMERS SUPER PAC
commidlist.append('C00457523') # WELLS FARGO BANK CUSTOMERS SUPER PAC
commidlist.append('C00456418') # WESTGATE RESORT CUSTOMERS SUPER PAC
commidlist.append('C00456467') # WHITE HOUSE EMPLOYEES SUPER PAC
commidlist.append('C00507525') # WINNING OUR FUTURE
commidlist.append('C00485102') # WOLF PAC
commidlist.append('C00456350') # YALE UNIVERSITY GRADUATES SUPER PAC
commidlist.append('C00504761') # YG ACTION FUND
commidlist.append('C00505248') # YOUR AMERICA INC

# Begin scrape
print 'Initializing FEC scrape...'
print 'Fetching data for ' + str(len(commidlist)) + ' committees.\n'

# Set up a list to house all available file IDs
filing_numbers = []

# Set a regular expression to match six-digit numbers
regex = re.compile(r'[0-9]{6}')

# For each committee id, open the page and read its HTML
for x in commidlist:
    print 'Searching files for ' + x + '.'
    url = "http://query.nictusa.com/cgi-bin/dcdev/forms/" + x + "/"
    html = urllib.urlopen(url)
    response = html.read()

    # For each line in the HTML, look for "Form F3" and a six-digit number
    # and build a list
    for line in response.splitlines():
        if re.search("Form F3", line) and re.search(regex, line):
            filing_numbers += re.findall(regex, line)

filing_numbers.sort()

# Create another list for file IDs to download
downloadlist = []

# Compile list of file IDs that have not been dowloaded previously
for x in filing_numbers:
    if fileidlist.count(x) == 0:
        downloadlist.append(x)

# File search completed
print '\nFile search completed. Beginning download...\n'

# For each retrieved filing number, download and save the files.
for y in downloadlist:
    filename = y + ".fec"
    print 'Downloading ' + filename + '.'
    url2 = "http://query.nictusa.com/dcdev/posted/" + filename
    urllib.urlretrieve(url2, savedir + filename)

# Display completion message
print 'File download complete!'
