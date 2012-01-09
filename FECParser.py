# FEC Parser
# By Christopher Schnaars, USA TODAY
# Developed with Python 2.7.2

"""
The purpose of this script is to parse ASCII-28 delimited text files
from the Federal Election Commission (FEC) containing campaign
contribution, expenditure, loan and other data from Form 3 reports filed
by candidate committees, political action committees (PACs) and
other organizations.

If you enable the script's database functionality, header rows are added
to Form F3 tables in a database mamager.

Regardless of whether you use database integration, the Image ID for
each file (the unique ID assigned to each file by the FEC) is prepended
to each data row.

This script presently supports only header versions 6.4, 7.0 and 8.0.
Files with unsupported headers are moved to the review directory.

Child rows with unrecognizable codes in the first (FormType) column
are saved to a timestamped "review" file saved in the review directory.

For complete documentation, see the README file.
"""

# User variables

# Try to import your user settings or set them explicitly. The database
# connection string will be ignored if database integration is disabled.
try:
    exec(open('usersettings.py').read())
except:
    maindir = 'C:\\data\\Python\\FEC\\'
    connstr = 'DRIVER={SQL Server};SERVER=;DATABASE=FEC;UID=;PWD=;'

# You can alter these to customize file locations
sourcedir = maindir + 'Import\\'
destdir = maindir + 'Processed\\'
outputdir = maindir + 'Output\\'
reviewdir = maindir + 'Review\\'

# Database integration flag
# Set to 1 to integrate with your database.
# Set to 0 to disable this functionality
usedatabaseflag = 0

# Script variables
delimiter = chr(28)

# Import needed libraries
import os, glob, time, linecache, shutil

# Create text files for data dump
try:
    timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
    scheduleafile = outputdir + 'ScheduleAImport_' + timestamp + '.txt'
    schedulebfile = outputdir + 'ScheduleBImport_' + timestamp + '.txt'
    schedulecfile = outputdir + 'ScheduleCImport_' + timestamp + '.txt'
    schedulec1file = outputdir + 'ScheduleC1Import_' + timestamp + '.txt'
    schedulec2file = outputdir + 'ScheduleC2Import_' + timestamp + '.txt'
    scheduledfile = outputdir + 'ScheduleDImport_' + timestamp + '.txt'
    scheduleefile = outputdir + 'ScheduleEImport_' + timestamp + '.txt'
    textfile = outputdir + 'TextImport_' + timestamp + '.txt'
    reviewfile = reviewdir + 'Review_' + timestamp + '.txt'

    sched_a_file = open(scheduleafile, 'w')
    sched_b_file = open(schedulebfile, 'w')
    sched_c_file = open(schedulecfile, 'w')
    sched_c1_file = open(schedulec1file, 'w')
    sched_c2_file = open(schedulec2file, 'w')
    sched_d_file = open(scheduledfile, 'w')
    sched_e_file = open(scheduleefile, 'w')
    text_file = open(textfile, 'w')
    review_file = open(reviewfile, 'w')

    # Create column headers
    scheduleaheaderstring = 'ParentType\tImageId\tFormType\tCommID\tTransID\tBackRefTransID\tBackRefSchedName\t' \
                   'EntityType\tContOrgName\tContLastName\tContFirstName\tContMidName\t' \
                   'ContPrefix\tContSuffix\tContAddress1\tContAddress2\tContCity\tContState\t' \
                   'ContZip\tElecCode\tElecOtherDesc\tstrContDate\tContAmount\tContAggregate\t' \
                   'ContPurposeCode\tContPurposeDesc\tContEmployer\tContOccupation\t' \
                   'DonorCommFECID\tDonorCommName\tDonorCandFECID\tDonorCandLastName\t' \
                   'DonorCandFirstName\tDonorCandMidName\tDonorCandPrefix\tDonorCandSuffix\t' \
                   'DonorCandOffice\tDonorCandState\tDonorCandDist\tConduitName\t' \
                   'ConduitAddress1\tConduitAddress2\tConduitCity\tConduitState\tConduitZip\t' \
                   'MemoCode\tMemoText\n'
    schedulebheaderstring = 'ParentType\tImageId\tFormType\tFilerCommID\tTransID\tBackRefTransID\tBackRefSchedName\t' \
                    'EntityType\tPayeeOrgName\tPayeeLastName\tPayeeFirstName\tPayeeMidName\t' \
                    'PayeePrefix\tPayeeSuffix\tPayeeAddress1\tPayeeAddress2\tPayeeCity\t' \
                    'PayeeState\tPayeeZip\tElecCode\tElecOtherDesc\tstrExpDate\tExpAmount\t' \
                    'SemiAnnRefundedBundledAmt\tExpPurpCode\tExpPurpDesc\tCatCode\tBenCommFECID\t' \
                    'BenCommName\tBenCandFECID\tBenCandLastName\tBenCandFirstName\tBenCandMidName\t' \
                    'BenCandPrefix\tBenCandSuffix\tBenCandOffice\tBenCandState\tBenCandDist\t' \
                    'ConduitName\tConduitAddress1\tConduitAddress2\tConduitCity\tConduitState\t' \
                    'ConduitZip\tMemoCode\tMemoText\n'
    schedulecheaderstring = 'ParentType\tImageId\tFormType\tFilerCommID\tTransID\tRectLineNbr\tEntityType\t' \
                    'LenderOrgName\tLenderLastName\tLenderFirstName\tLenderMidName\t' \
                    'LenderPrefix\tLenderSuffix\tLenderAddress1\tLenderAddress2\t' \
                    'LenderCity\tLenterState\tLenderZip\tElecCod\tElecOtherDesc\t' \
                    'LoanAmt\tLoanPymtToDate\tLoanBal\tstrLoanIncurredDate\t' \
                    'strLoanDueDate\tLoanIntRate\tLoanSecuredFlag\tLoanPersFundsFlag\t' \
                    'LenderCommID\tLenderCandID\tLenderCandLastName\tLenderCandFirstName\t' \
                    'LenderCandMidName\tLenderCandPrefix\tLenderCandSuffix\tLenderCandOffice\t' \
                    'LenderCandState\tLenderCandDist\tMemoCode\tMemoText\n'
    schedulec1headerstring = 'ParentType\tImageId\tFormType\tFilerCommID\tTransID\tBackRefTransID\t' \
                    'LenderOrgName\tLenderAddress1\tLenderAddress2\tLenderCity\t' \
                    'LenderState\tLenderZip\tLoanAmt\tLoanIntRate\tstrLoanIncurredDate\t' \
                    'strLoanDueDate\tA1_LoanRestructuredFlag\tA2_strOrigLoanIncurredDate\t' \
                    'B1_CreditAmtThisDraw\tB2_TotBalance\tC_OthersLiableFlag\t' \
                    'D_CollateralFlag\tD1_CollateralDescription\tD2_CollateralValue\t' \
                    'D3_PerfectedInterestFlag\tE1_FutureIncomeFlag\tE2_FutureIncomeDesc\t' \
                    'E3_EstimatedValue\tE4_strDepositoryAcctEstablishedDate\tE5_AcctLocName\t' \
                    'E6_AcctAddress1\tE7_AcctAddress1\tE8_AcctCity\tE9_State\tE10_Zip\t' \
                    'E11_strDepositAcctAuthDate\tF_LoanBasisDesc\tG_TreasLastName\t' \
                    'G_TreasFirstName\tG_TreasMidName\tG_TreasPrefix\tG_TreasSuffix\t' \
                    'G_strDateSigned\tH_AuthorizedLastName\tH_AuthorizedfirstName\t' \
                    'H_AuthorizedMidName\tH_AuthorizedPrefix\tH_AuthorizedSuffix\t' \
                    'H_AuthorizedTitle\tH_strDateSigned\n'
    schedulec2headerstring = 'ParentType\tImageId\tFormType\tFilerCommID\tTransID\tBackRefTransID\t' \
                    'GuarLastName\tGuarFirstName\tGuarMidName\tGuarPrefix\t' \
                    'GuarSuffix\tGuarAddress1\tGuarAddress2\tGuarCity\tGuarState\t' \
                    'GuarZip\tGuarEmployer\tGuarOccupation\tGuarAmt\n'
    scheduledheaderstring = 'ParentType\tImageId\tFormType\tCommID\tTransID\tEntityType\tCredOrgName\t' \
                    'CredLastName\tCredFirstName\tCredMidName\tCredPrefix\t' \
                    'CredSuffix\tCredAddress1\tCredAddress2\tCredCity\tCredState\t' \
                    'CredZip\tDebtPurpose\tBegBal_Prd\tIncurredAmt_Prd\tPaymtAmt_Prd\t' \
                    'BalanceAtClose_Prd\n'
    scheduleeheaderstring = 'ParentType\tImageId\tFormType\tFilerCommID\tTransID\tBackRefTransID\t' \
                    'BackRefSchedName\tEntityType\tPayeeOrgName\tPayeeLastName\t' \
                    'PayeeFirstName\tPayeeMidName\tPayeePrefix\tPayeeSuffix\t' \
                    'PayeeAddress1\tPayeeAddress2\tPayeeCity\tPayeeState\tPayeeZip\t' \
                    'ElecCode\tElecOtherDesc\tstrExpDate\tExpAmount\tCalYTD\t' \
                    'ExpPurpCode\tExpPurpDesc\tCatCode\tPayeeCommFECID\tSuppOppCode\t' \
                    'SuppOppCandID\tSuppOppCandLastName\tSuppOppCandFirstName\t' \
                    'SuppOppCandMidName\tSuppOppCandPrefix\tSuppOppCandSuffix\t' \
                    'SuppOppCandOffice\tSuppOppCandState\tSuppOppCandDist\t' \
                    'CompLastName\tCompFirstName\tCompMidName\tCompPrefix\tCompSuffix\t' \
                    'strDateSigned\tMemoCode\tMemoText\n'
    textheaderstring = 'ParentType\tImageId\tRecType\tCommID\tTransID\tBackRefTransID\tBackRefFormName\tFullText\n'

    # Write headers to output files
    sched_a_file.write(scheduleaheaderstring)
    sched_b_file.write(schedulebheaderstring)
    sched_c_file.write(schedulecheaderstring)
    sched_c1_file.write(schedulec1headerstring)
    sched_c2_file.write(schedulec2headerstring)
    sched_d_file.write(scheduledheaderstring)
    sched_e_file.write(scheduleeheaderstring)
    text_file.write(textheaderstring)

    # Import appropriate library if database integration is enabled.
    # Otherwise, create text files to house headers.
    if usedatabaseflag == 1:

        # import necessary library
        import pyodbc # SQL Server

    else:
        formf3headerfile = outputdir + 'FormF3Headers_' + timestamp + '.txt'
        formf3pheaderfile = outputdir + 'FormF3PHeaders_' + timestamp + '.txt'
        formf3xheaderfile = outputdir + 'FormF3XHeaders_' + timestamp + '.txt'

        form_f3_file = open(formf3headerfile, 'w')
        form_f3p_file = open(formf3pheaderfile, 'w')
        form_f3x_file = open(formf3xheaderfile, 'w')

        formf3headerstring = 'ImageID\tFormType\tCommID\tCommName\t' \
            'AddressChange\tCommAddress1\tCommAddress2\tCommCity\tCommState\t' \
            'CommZip\tElecState\tElecDist\tReptCode\tElecCode\tstrElecDate\t' \
            'StateOfElec\tstrCovgFromDate\tstrCovgToDate\tTreasLastName\t' \
            'TreasFirstName\tTreasMidName\tTreasPrefix\tTreasSuffix\tstrDateSigned\t' \
            'Line6a_TotalContribs_Prd\tLine6b_TotalContribRefunds_Prd\t' \
            'Line6c_NetContribs_Prd\tLine7a_TotOpExps_Prd\tLine7b_TotOffsetToOpExps_Prd\t' \
            'Line7c_NetOpExps_Prd\tLine8_CashOnHandAtClose_Prd\tLine9_DebtsTo_Prd\t' \
            'Line10_DebtsBy_Prd\tLine11a1_IndivsItemized_Prd\tLine11a2_IndivsUnitemized_Prd\t' \
            'Line11a3_IndivsContribTotal_Prd\tLine11b_PolPtyComms_Prd\tLine11c_OtherPACs_Prd\t' \
            'Line11d_Candidate_Prd\tLine11e_TotalContribs_Prd\tLine12_TransfersFrom_Prd\t' \
            'Line13a_LoansByCand_Prd\tLine13b_OtherLoans_Prd\tLine13c_TotLoans_Prd\t' \
            'Line14_OffsetsToOpExps_Prd\tLine15_OtherReceipts_Prd\tLine16_TotReceipts_Prd\t' \
            'Line17_OpExps_Prd\tLine18_TransToOtherComms_Prd\tLine19a_LoanRepaymts_Cand_Prd\t' \
            'Line19b_LoanRepaymts_Other_Prd\tLine19c_TotLoanRepaymts_Prd\t' \
            'Loan20a_IndivRefunds_Prd\tLine20b_PolPartyCommRefunds_Prd\t' \
            'Line20c_OtherPolCommRefunds_Prd\tLine20d_TotContRefunds_Prd\t' \
            'Line21_OtherDisb_Prd\tLine22_TotDisb_Prd\tLine23_CashBegin_Prd\t' \
            'Line24_TotReceipts_Prd\tLine25_Subtotal\tLine26_TotDisbThisPrd_Prd\t' \
            'Line27_CashAtClose_Prd\tLine6a_TotalContribs_Tot\t' \
            'Line6b_TotalContribRefunds_Tot\tLine6c_NetContribs_Tot\tLine7a_TotOpExps_Tot\t' \
            'Line7b_TotOffsetToOpExps_Tot\tLine7c_NetOpExps_Tot\t' \
            'Line11a1_IndivsItemized_Tot\tLine11a2_IndivsUnitemized_Tot\t' \
            'Line11a3_IndivsContribTotal_Tot\tLine11b_PolPtyComms_Tot\t' \
            'Line11c_OtherPACs_Tot\tLine11d_Candidate_Tot\tLine11e_TotalContribs_Tot\t' \
            'Line12_TransfersFrom_Tot\tLine13a_LoansByCand_Tot\tLine13b_OtherLoans_Tot\t' \
            'Line13c_TotLoans_Tot\tLine14_OffsetsToOpExps_Tot\tLine15_OtherReceipts_Tot\t' \
            'Line16_TotReceipts_Tot\tLine17_OpExps_Tot\tLine18_TransToOtherComms_Tot\t' \
            'Line19a_LoanRepaymts_Cand_Tot\tLine19b_LoanRepaymts_Other_Tot\t' \
            'Line19c_TotLoanRepaymts_Tot\tLoan20a_IndivRefunds_Tot\t' \
            'Line20b_PolPartyCommRefunds_Tot\tLine20c_OtherPolCommRefunds_Tot\t' \
            'Line20d_TotContRefunds_Tot\tLine21_OtherDisb_Tot\tLine22_TotDisb_Tot\n'
        formf3pheaderstring = 'ImageID\tFormType\tCommID\tCommName\t' \
            'AddressChange\tCommAddress1\tCommAddress2\tCommCity\tCommState\t' \
            'CommZip\tActivityPrim\tActivityGen\tReptCode\tElecCode\t' \
            'strElecDate\tElecState\tstrFromDate\tstrToDate\tTreasLastName\t' \
            'TreasFirstName\tTreasMidName\tTreasPrefix\tTreasSuffix\t' \
            'strDateSigned\tLine6_CashBegin\tLine7_TotReceipts\t' \
            'Line8_Subtotal\tLine9_TotalDisb\tLine10_CashClose\t' \
            'Line11_DebtsTo\tLine12_DebtsBy\tLine13_ExpendsSubToLimits\t' \
            'Line14_NetContribs\tLine15_NetOpExps\tLine16_FedFunds_Prd\t' \
            'Line17a1_IndivsItemzd_Prd\tLine17a2_IndivsUnItemzd_Prd\t' \
            'Line17a3_IndContTot_Prd\tLine17b_PolPartyComms_Prd\t' \
            'Line17c_OtherPACs_Prd\tLine17d_Candidate_Prd\t' \
            'Line17e_TotContribs_Prd\tLine18_TransfersFrom_Prd\t' \
            'Line19a_CandLoans_Prd\tLine19b_OtherLoans_Prd\t' \
            'Line19c_TotLoans_Prd\tLine20a_Operating_Prd\t' \
            'Line20b_Fundraising_Prd\tLine20c_LegalAcctg_Prd\t' \
            'Line20d_TotExpOffsets_Prd\tLine21_OtherReceipts_Prd\t' \
            'Line22_TotReceipts_Prd\tLine23_OpExpends_Prd\t' \
            'Line24_TransToOtherComms_Prd\tLine25_FundraisingDisbursed_Prd\t' \
            'Line26_ExemptLegalAcctgDisb_Prd\tLine27a_CandRepymts_Prd\t' \
            'Line27b_OtherRepymts_Prd\tLine27c_TotLoanRepymts_Prd\t' \
            'Line28a_IndivRefunds_Prd\tLine28b_PolPartyCommRefunds_Prd\t' \
            'Line28c_OtherPolCommRefunds_Prd\tLine28d_TotalContRefunds_Prd\t' \
            'Line29_OtherDisb_Prd\tLine30_TotDisb_Prd\t' \
            'Line31_ItemsToLiq_Prd\tAllocAlabama_Prd\tAllocAlaska_Prd\t' \
            'AllocArizona_Prd\tAllocArkansas_Prd\tAllocCalifornia_Prd\t' \
            'AllocColorado_Prd\tAllocConnecticut_Prd\tAllocDelaware_Prd\t' \
            'AllocDistCol_Prd\tAllocFlorida_Prd\tAllocGeorgia_Prd\t' \
            'AllocHawaii_Prd\tAllocIdaho_Prd\tAllocIllinois_Prd\t' \
            'AllocIndiana_Prd\tAllocIowa_Prd\tAllocKansas_Prd\t' \
            'AllocKentucky_Prd\tAllocLouisiana_Prd\tAllocMaine_Prd\t' \
            'AllocMaryland_Prd\tAllocMassachusetts_Prd\tAllocMichigan_Prd\t' \
            'AllocMinnesota_Prd\tAllocMississippi_Prd\tAllocMissouri_Prd\t' \
            'AllocMontana_Prd\tAllocNebraska_Prd\tAllocNevada_Prd\t' \
            'AllocNewHampshire_Prd\tAllocNewJersey_Prd\tAllocNewMexico_Prd\t' \
            'AllocNewYork_Prd\tAllocNorthCarolina_Prd\t' \
            'AllocNorthDakota_Prd\tAllocOhio_Prd\tAllocOklahoma_Prd\t' \
            'AllocOregon_Prd\tAllocPennsylvania_Prd\tAllocRhodeIsland_Prd\t' \
            'AllocSouthCarolina_Prd\tAllocSouthDakota_Prd\t' \
            'AllocTennessee_Prd\tAllocTexas_Prd\tAllocUtah_Prd\t' \
            'AllocVermont_Prd\tAllocVirginia_Prd\tAllocWashington_Prd\t' \
            'AllocWestVirginia_Prd\tAllocWisconsin_Prd\tAllocWyoming_Prd\t' \
            'AllocPuertoRico_Prd\tAllocGuam_Prd\tAllocVirginIslands_Prd\t' \
            'AllocStatesTotal_Prd\tLine16_FedFunds_Tot\t' \
            'Line17a1_IndivsItemzd_Tot\tLine17a2_IndivsUnItemzd_Tot\t' \
            'Line17a3_IndContTot_Tot\tLine17b_PolPartyComms_Tot\t' \
            'Line17c_OtherPACs_Tot\tLine17d_Candidate_Tot\t' \
            'Line17e_TotContribs_Tot\tLine18_TransfersFrom_Tot\t' \
            'Line19a_CandLoans_Tot\tLine19b_OtherLoans_Tot\t' \
            'Line19c_TotLoans_Tot\tLine20a_Operating_Tot\t' \
            'Line20b_Fundraising_Tot\tLine20c_LegalAcctg_Tot\t' \
            'Line20d_TotExpOffsets_Tot\tLine21_OtherReceipts_Tot\t' \
            'Line22_TotReceipts_Tot\tLine23_OpExpends_Tot\t' \
            'Line24_TransToOtherComms_Tot\tLine25_FundraisingDisbursed_Tot\t' \
            'Line26_ExemptLegalAcctgDisb_Tot\tLine27a_CandRepymts_Tot\t' \
            'Line27b_OtherRepymts_Tot\tLine27c_TotLoanRepymts_Tot\t' \
            'Line28a_IndivRefunds_Tot\tLine28b_PolPartyCommRefunds_Tot\t' \
            'Line28c_OtherPolCommRefunds_Tot\t' \
            'Line28d_TotalContRefunds_Tot\tLine29_OtherDisb_Tot\t' \
            'Line30_TotDisb_Tot\tAllocAlabama_Tot\tAllocAlaska_Tot\t' \
            'AllocArizona_Tot\tAllocArkansas_Tot\tAllocCalifornia_Tot\t' \
            'AllocColorado_Tot\tAllocConnecticut_Tot\tAllocDelaware_Tot\t' \
            'AllocDistCol_Tot\tAllocFlorida_Tot\tAllocGeorgia_Tot\t' \
            'AllocHawaii_Tot\tAllocIdaho_Tot\tAllocIllinois_Tot\t' \
            'AllocIndiana_Tot\tAllocIowa_Tot\tAllocKansas_Tot\t' \
            'AllocKentucky_Tot\tAllocLouisiana_Tot\tAllocMaine_Tot\t' \
            'AllocMaryland_Tot\tAllocMassachusetts_Tot\t' \
            'AllocMichigan_Tot\tAllocMinnesota_Tot\tAllocMississippi_Tot\t' \
            'AllocMissouri_Tot\tAllocMontana_Tot\tAllocNebraska_Tot\t' \
            'AllocNevada_Tot\tAllocNewHampshire_Tot\tAllocNewJersey_Tot\t' \
            'AllocNewMexico_Tot\tAllocNewYork_Tot\tAllocNorthCarolina_Tot\t' \
            'AllocNorthDakota_Tot\tAllocOhio_Tot\tAllocOklahoma_Tot\t' \
            'AllocOregon_Tot\tAllocPennsylvania_Tot\tAllocRhodeIsland_Tot\t' \
            'AllocSouthCarolina_Tot\tAllocSouthDakota_Tot\t' \
            'AllocTennessee_Tot\tAllocTexas_Tot\tAllocUtah_Tot\t' \
            'AllocVermont_Tot\tAllocVirginia_Tot\tAllocWashington_Tot\t' \
            'AllocWestVirginia_Tot\tAllocWisconsin_Tot\tAllocWyoming_Tot\t' \
            'AllocPuertoRico_Tot\tAllocGuam_Tot\tAllocVirginIslands_Tot\t' \
            'AllocStatesTotal_Tot\n'
        formf3xheaderstring = 'ImageID\tFormType\tCommID\t' \
            'CommName\tAddressChange\tCommAddress1\tCommAddress2\t' \
            'CommCity\tCommState\tCommZip\tReptCode\tElecCode\t' \
            'strElecDate\tElecState\tstrFromDate\tstrToDate\t' \
            'flgQualifiedComm\tTreasLastName\tTreasFirstName\t' \
            'TreasMidName\tTreasPrefix\tTreasSuffix\tstrDateSigned\t' \
            'Line6b_CashBegin_Prd\tLine6c_TotalRects_Prd\t' \
            'Line6d_CashBeginSubtotal_Prd\tLine7_TotDisbmts_Prd\t' \
            'Line8_CashOnHandAtClose_Prd\tLine9_DebtsTo_Prd\t' \
            'Line10_DebtsBy_Prd\tLine11a1_Itemized_Prd\t' \
            'Line11a2_Unitemized_Prd\tLine11a3_Total_Prd\t' \
            'Line11b_PolPtyComms_Prd\tLine11c_OtherPACs_Prd\t' \
            'Line11d_TotalContribs_Prd\tLine12_TransfersFrom_Prd\t' \
            'Line13_AllLoansRcvd_Prd\tLine14_LoanRepymtsRecv_Prd\t' \
            'Line15_OffsetsToOpExps_Refunds_Prd\t' \
            'Line16_RefundsOfFedContribs_Prd\t' \
            'Line17_OtherFedRects_Divds_Prd\t' \
            'Line18a_TransfersFromNonFedAcct_H3_Prd\t' \
            'Line18b_TransfersFromNonFed_LevinH5_Prd\t' \
            'Line18c_TotalNonFedTransfers_Prd\t' \
            'Line19_TotalReceipts_Prd\tLine20_TotalFedReceipts_Prd\t' \
            'Line21a1_FedShare_Prd\tLine21a2_NonFedShare_Prd\t' \
            'Line21b_OtherFedOpExps_Prd\tLine21c_TotOpExps_Prd\t' \
            'Line22_TransToOtherComms_Prd\t' \
            'Line23_ContribsToFedCandsOrComms_Prd\t' \
            'Line24_IndptExps_Prd\tLine25_CoordtdExpByPrtyComms_Prd\t' \
            'Line26_LoanRepayments_Prd\tLine27_LoansMade_Prd\t' \
            'Line28a_IndivRefunds_Prd\t' \
            'Line28b_PolPartyCommRefunds_Prd\t' \
            'Line28c_OtherPolCommRefunds_Prd\t' \
            'Line28d_TotalContRefunds_Prd\tLine29_OtherDisb_Prd\t' \
            'Line30a1_SharedFedActH6FedShare_Prd\t' \
            'Line30a2_SharedFedActH6NonFed_Prd\t' \
            'Line30b_NonAlloc100PctFedElecActivity_Prd\t' \
            'Line30c_TotFedElecActivity_Prd\tLine31_TotDisbmts_Prd\t' \
            'Line32_TotFedDisbmts_Prd\tLine33_TotContribs_Prd\t' \
            'Line34_TotContribRefunds_Prd\tLine35_NetContribs_Prd\t' \
            'Line36_TotFedOpExps_Prd\tLine37_OffsetsToOpExps_Prd\t' \
            'Line38_NetOpExps_Prd\tLine6b_CashBegin_Tot\tLine6b_Year\t' \
            'Line6c_TotalRects_Tot\tLine6d_CashBeginSubtotal_Tot\t' \
            'Line7_TotDisbmts_Tot\tLine8_CashOnHandAtClose_Tot\t' \
            'Line11a1_Itemized_Tot\tLine11a2_Unitemized_Tot\t' \
            'Line11a3_Total_Tot\tLine11b_PolPtyComms_Tot\t' \
            'Line11c_OtherPACs_Tot\tLine11d_TotalContribs_Tot\t' \
            'Line12_TransfersFrom_Tot\tLine13_AllLoansRcvd_Tot\t' \
            'Line14_LoanRepymtsRecv_Tot\t' \
            'Line15_OffsetsToOpExps_Refunds_Tot\t' \
            'Line16_RefundsOfFedContribs_Tot\t' \
            'Line17_OtherFedRects_Divds_Tot\t' \
            'Line18a_TransfersFromNonFedAcct_H3_Tot\t' \
            'Line18b_TransfersFromNonFed_LevinH5_Tot\t' \
            'Line18c_TotalNonFedTransfers_Tot\t' \
            'Line19_TotalReceipts_Tot\tLine20_TotalFedReceipts_Tot\t' \
            'Line21a1_FedShare_Tot\tLine21a2_NonFedShare_Tot\t' \
            'Line21b_OtherFedOpExps_Tot\tLine21c_TotOpExps_Tot\t' \
            'Line22_TransToOtherComms_Tot\t' \
            'Line23_ContribsToFedCandsOrComms_Tot\t' \
            'Line24_IndptExps_Tot\tLine25_CoordtdExpByPrtyComms_Tot\t' \
            'Line26_LoanRepayments_Tot\tLine27_LoansMade_Tot\t' \
            'Line28a_IndivRefunds_Tot\t' \
            'Line28b_PolPartyCommRefunds_Tot\t' \
            'Line28c_OtherPolCommRefunds_Tot\t' \
            'Line28d_TotalContRefunds_Tot\tLine29_OtherDisb_Tot\t' \
            'Line30a1_SharedFedActH6FedShare_Tot\t' \
            'Line30a2_SharedFedActH6NonFed_Tot\t' \
            'Line30b_NonAlloc100PctFedElecActivity_Tot\t' \
            'Line30c_TotFedElecActivity_Tot\tLine31_TotDisbmts_Tot\t' \
            'Line32_TotFedDisbmts_Tot\tLine33_TotContribs_Tot\t' \
            'Line34_TotContribRefunds_Tot\tLine35_NetContribs_Tot\t' \
            'Line36_TotFedOpExps_Tot\tLine37_OffsetsToOpExps_Tot\t' \
            'Line38_NetOpExps_Tot\n'

        form_f3_file.write(formf3headerstring)
        form_f3p_file.write(formf3pheaderstring)
        form_f3x_file.write(formf3xheaderstring)

    # Iterate through all files in the source directory
    # and process those with .fec extension
    try:
        for datafile in glob.glob(os.path.join(sourcedir, '*.fec')):
            filename = datafile.replace(sourcedir, '')
            print 'Processing: ' + filename

            # Store file ID in variable
            imageid = filename.replace('.fec','')

            # Grab first two lines
            hdr1 = linecache.getline(datafile, 1)
            hdr1list = hdr1.split(delimiter)
            hdr2 = linecache.getline(datafile, 2)
            hdr2list = hdr2.split(delimiter)
            
            # Check header version
            # Presently, only 6.4, 7.0 and 8.0 are supported
            if hdr1list[0].strip('"') == 'HDR':
                headerversion = hdr1list[2].strip('"').strip()
            else:
                shutil.move(datafile, reviewdir + filename.replace('.fec','_INV_HDR.fec'))
                continue

            if headerversion != '6.4' and headerversion !='7.0' and headerversion !='8.0':
                shutil.move(datafile, reviewdir + filename.replace('.fec','_HDR_' + headerversion + '.fec'))
                continue

            # Header 1 is valid, so now let's parse line 2.
            # First, retrieve form type
            formtype = hdr2list[0].strip('"')
            
            # Make sure form type is valid
            # Supported:
            #   F3: F3A, F3N
            #   F3P: F3PA, F3PN
            #   F3X: F3XA, F3XN
            if formtype != 'F3A' and formtype != 'F3N' \
               and formtype != 'F3PA' and formtype != 'F3PN'\
               and formtype != 'F3XA' and formtype != 'F3XN':
                    shutil.move(datafile, reviewdir + filename.replace('.fec','_INV_FORMTYPE_' + formtype + '.fec'))
                    continue

            # At this point, the header is valid.
            # Run custom code to ensure various header types conform.
            
            # Header 6.4, Forms F3PA and F3PN
            if headerversion == '6.4' and formtype.startswith('F3P'):

                # 6.4 does not have separate values for line 17a, so we
                # need to insert blank values for 17a1 and 17a2 and leave
                # the reported values (period and total) for 17a3.
                cols = hdr2.split(delimiter)
                cols.insert(34, '')
                cols.insert(34, '')
                cols.insert(121, '')
                cols.insert(121, '')

                # Convert list back to string
                hdr2 = delimiter.join(map(str, cols))

            # Generic cleanup of header lines
            
            # Change all tabs and newlines to spaces
            lineclean = hdr2.expandtabs(1).replace('\r',' ').replace('\n',' ')
            # Remove leading and trailing whitespace
            lineclean = lineclean.strip()
            # Remove all instances of two spaces
            while '  ' in lineclean:
                lineclean = lineclean.replace('  ',' ')
            # Remove spaces immediately before or after a delimiter
            while ' ' + delimiter in lineclean:
                lineclean = lineclean.replace(' ' + delimiter, delimiter)
            while delimiter + ' ' in lineclean:
                lineclean = lineclean.replace(delimiter + ' ', delimiter)
            # Remove leading and trailing quotation marks
            while lineclean.startswith('"') or lineclean.endswith('"') or lineclean.startswith("'") or lineclean.endswith("'"):
                lineclean = lineclean.strip().strip('"').strip("'").strip()
            # Remove double quotation marks when immediately before or after a delimiter.
            while '"' + delimiter in lineclean:
                lineclean = lineclean.replace('"' + delimiter, delimiter)
            while delimiter + '"' in lineclean:
                lineclean = lineclean.replace(delimiter + '"', delimiter)
            # Remove single quotation marks when immediately before or after a delimiter.
            while "'" + delimiter in lineclean:
                lineclean = lineclean.replace("'" + delimiter, delimiter)
            while delimiter + "'" in lineclean:
                lineclean = lineclean.replace(delimiter + "'", delimiter)
            # Replace '' between two delimiters with just two delimiters
            lineclean = lineclean.replace(delimiter + "''" + delimiter, delimiter + delimiter)
            # Replace all cases of '' with "
            while "''" in lineclean:
                lineclean = lineclean.replace("''", '"')
            # Replace all cases of "" with "
            while '""' in lineclean:
                lineclean = lineclean.replace('""', '"')
            # Change all instances of ' to ''
            lineclean = lineclean.replace("'", "''")
            # Insert NULL between delimiters
            while delimiter + delimter in lineclean:
                lineclean = lineclean.replace(delimiter + delimiter, delimiter + 'NULL' + delimiter)
            # Add image id
            lineclean = "'" + imageid + delimiter + lineclean
            # Replace delimiters with single quotations and commas
            if usedatabaseflag == 1:
                lineclean = lineclean.replace(delimiter, "','")
                if lineclean.endswith(",'"):
                    lineclean = lineclean[:-2]
            else:
                lineclean = lineclean.replace(delimiter, "'\t'")
                if lineclean.endswith("\t'"):
                    lineclean = lineclean[:-2]
            # Remove ' from around NULL
            lineclean = lineclean.replace(",'NULL'",',NULL').replace("\t'NULL'",'\tNULL')
            # Make sure last field has closing '
            if not lineclean.endswith("'") and not lineclean.endswith('NULL'):
                lineclean += "'"
            
            # If database integration has been enabled, send header info
            # to the database manager. Note that you will need to modify
            # this code if you are not using SQL Server, which processes
            # this data with stored procedure calls.

            # When the script is NOT integrated with a database, the file ID
            # (imageid) is prefixed to each child row.
            if usedatabaseflag == 1:

                # Create stored procedure call
                sql = 'EXEC '

                # Add appropriate stored procedure
                if formtype == 'F3A' or formtype == 'F3N':
                    sql += "dbo.usp_AddF3Header"
                elif formtype == 'F3PA' or formtype == 'F3PN':
                    sql += "dbo.usp_AddF3PHeader"
                elif formtype == 'F3XA' or formtype == 'F3XN':
                    sql += "dbo.usp_AddF3XHeader"

                # Build final sql string, with new line
                sql += ' ' + lineclean + '\n'

                # Create SQL Server connection
                conn = pyodbc.connect(connstr)
                cursor = conn.cursor()

                # Excecute stored procedure
                cursor.execute(sql)
                sqlresult = cursor.fetchone()
                fileid = sqlresult[0]
                conn.commit()
                conn.close()

                # Alert user if file may have been previously imported
                # and move to review directory
                if fileid == -1:
                    print 'This file may already be in the FEC database, so the ' \
                          'header was not imported. See the Review directory.\n'
                    raw_input('Press Enter to continue...')
                    shutil.move(datafile, reviewdir + filename)
                    print '\n'
                    continue

            # Otherwise, database integration disabled;
            # Store ImageID as FileID
            # and copy second header line to header text file.
            else:

                # Write header to appropriate file
                if lineclean.startswith("'"):
                    lineclean = lineclean[1:]
                if lineclean.endswith("'"):
                    lineclean = lineclean[:-1]
                lineclean += '\n'
                lineclean = lineclean.replace("'\t","\t").replace("\t'","\t")
                colct = len(lineclean.split('\t'))
                if formtype == 'F3A' or formtype == 'F3N':
                    while colct < 94:
                        lineclean = lineclean.replace('\n', '\t\n')
                        colct = len(lineclean.split('\t'))
                    while colct > 94 and lineclean.endswith('\t\n'):
                        lineclean = lineclean[:-2] + '\n'
                        colct = len(lineclean.split('\t'))
                    if colct == 94:
                        form_f3_file.write(lineclean)
                    else:
                        print 'The header row for ' + filename + ' does not have ' \
                              'the correct number of columns. This file will be ' \
                              'moved to the review directory and will not ' \
                              'be imported.\n'
                        raw_input('Press Enter to continue...')
                        shutil.move(datafile, reviewdir + filename)
                        print '\n'
                        continue
                elif formtype == 'F3PA' or formtype == 'F3PN':
                    while colct < 207:
                        lineclean = lineclean.replace('\n', '\t\n')
                        colct = len(lineclean.split('\t'))
                    while colct > 207 and lineclean.endswith('\t\n'):
                        lineclean = lineclean[:-2] + '\n'
                        colct = len(lineclean.split('\t'))
                    if colct == 207:
                        form_f3p_file.write(lineclean)
                    else:
                        print 'The header row for ' + filename + ' does not have ' \
                              'the correct number of columns. This file will be ' \
                              'moved to the review directory and will not ' \
                              'be imported.\n'
                        raw_input('Press Enter to continue...')
                        shutil.move(datafile, reviewdir + filename)
                        print '\n'
                        continue
                elif formtype == 'F3XA' or formtype == 'F3XN':
                    while colct < 124:
                        lineclean = lineclean.replace('\n', '\t\n')
                        colct = len(lineclean.split('\t'))
                    while colct > 124 and lineclean.endswith('\t\n'):
                        lineclean = lineclean[:-2] + '\n'
                        colct = len(lineclean.split('\t'))
                    if colct == 124:
                        form_f3x_file.write(lineclean)
                    else:
                        print 'The header row for ' + filename + ' does not have ' \
                              'the correct number of columns. This file will be ' \
                              'moved to the review directory and will not ' \
                              'be imported.\n'
                        raw_input('Press Enter to continue...')
                        shutil.move(datafile, reviewdir + filename)
                        print '\n'
                        continue
                else:
                        print 'An unexpected error occurred while processing the ' \
                              'header for ' + filename + '. This file has been ' \
                              'moved to the review directory and will not ' \
                              'be imported.\n'
                        raw_input('Press Enter to continue...')
                        shutil.move(datafile, reviewdir + filename)
                        print '\n'
                        continue

            # At this point, we have a valid header for a new file
            # Copy each subsequent line to the appropriate output file.
            for line in open(datafile, 'rb'):

                # If the row is just white space, skip it
                if line.replace('/n','').expandtabs(1).replace(' ','').replace('"','').replace("'",'').replace(delimiter,'').strip() == '':
                    continue

                # Skip this row if it's a header line
                linetest = line.replace(delimiter,'').replace('"','').replace("'",'').upper()
                if linetest.startswith('HDR') or linetest.startswith('F3'):
                    continue

                # THIS SECTION INCLUDES CUSTOM CODE TO MAKE SURE DIFFERENT HEADER VERSIONS CONFORM

                # Header 8.0:
                # -----------
                if headerversion == '8.0':
                    # Schedule A:
                    # -----------
                    # Contribution Purpose Code (field 23) removed
                    # Add placeholder
                    if linetest.startswith('SA'):
                        cols = line.split(delimiter)
                        cols.insert(22, '')
                        line = delimiter.join(map(str, cols))
                    
                    # Schedule B:
                    # -----------
                    # Expenditure Purpose Code (field 23) removed
                    # Add placeholder
                    elif linetest.startswith('SB'):
                        cols = line.split(delimiter)
                        cols.insert(22, '')
                        line = delimiter.join(map(str, cols)) 
                    
                    # Schedule E:
                    # -----------
                    # Expenditure Purpose Code (field 23) removed
                    # Add placeholder
                    elif linetest.startswith('SE'):
                        cols = line.split(delimiter)
                        cols.insert(22, '')
                        line = delimiter.join(map(str, cols)) 

                # Parse the line on the delimiter and put in a list
                cols = line.split(delimiter)

                # Add header type and ID
                # Old code: datarow = formtype + delimiter + str(fileid) + delimiter + line
                datarow = formtype + delimiter + str(imageid) + delimiter + line

                # Clean up the line
                # Change all tabs and newlines to spaces,
                # and strip leading/trailing whitespace
                datarow = datarow.replace('\t',' ').replace('\r',' ').replace('\n',' ').strip()

                # Remove leading and trailing whitespace
                # datarow = datarow.strip()
                # Remove all instances of two spaces
                while '  ' in datarow:
                    datarow = datarow.replace('  ',' ')
                # Remove spaces immediately before or after a delimiter
                while ' ' + delimiter in datarow:
                    datarow = datarow.replace(' ' + delimiter, delimiter)
                while delimiter + ' ' in datarow:
                    datarow = datarow.replace(delimiter + ' ', delimiter)
                # Remove leading and trailing quotation marks
                while datarow.startswith('"') or datarow.endswith('"') or datarow.startswith("'") or datarow.endswith("'"):
                    datarow = datarow.strip().strip('"').strip("'").strip()
                # Remove double quotation marks when immediately before or after a delimiter.
                while '"' + delimiter in datarow:
                    datarow = datarow.replace('"' + delimiter, delimiter)
                while delimiter + '"' in datarow:
                    datarow = datarow.replace(delimiter + '"', delimiter)
                # Remove single quotation marks when immediately before or after a delimiter.
                while "'" + delimiter in datarow:
                    datarow = datarow.replace("'" + delimiter, delimiter)
                while delimiter + "'" in datarow:
                    datarow = datarow.replace(delimiter + "'", delimiter)
                # Replace '' between two delimiters with just two delimiters
                datarow = datarow.replace(delimiter + "''" + delimiter, delimiter + delimiter)
				# Replace all cases of '' with "
                while "''" in datarow:
                    datarow = datarow.replace("''", '"')
                # Replace all cases of "" with "
                while '""' in datarow:
                    datarow = datarow.replace('""', '"')
                # Replace all delimiters with tabs and add newline
                datarow = datarow.replace(delimiter, '\t') + '\n'
 
                # Now write the data row to the appropriate file
                rowtype = cols[0].strip('"')
                colct = len(datarow.split('\t'))
                
                if rowtype.startswith('SA'):
                    while colct < 47:
                        datarow = datarow.replace('\n', '\t\n')
                        colct = len(datarow.split('\t'))
                    while colct > 47 and datarow.endswith('\t\n'):
                        datarow = datarow[:-2] + '\n'
                        colct = len(datarow.split('\t'))
                    if colct == 47:
                        sched_a_file.write(datarow)
                    else:
                        review_file.write(datarow)
                elif rowtype.startswith('SB'):
                    while colct < 46:
                        datarow = datarow.replace('\n', '\t\n')
                        colct = len(datarow.split('\t'))
                    while colct > 46 and datarow.endswith('\t\n'):
                        datarow = datarow[:-2] + '\n'
                        colct = len(datarow.split('\t'))
                    if colct == 46:
                        sched_b_file.write(datarow)
                    else:
                        review_file.write(datarow)
                elif rowtype.startswith('SC/'):
                    while colct < 40:
                        datarow = datarow.replace('\n', '\t\n')
                        colct = len(datarow.split('\t'))
                    while colct > 40 and datarow.endswith('\t\n'):
                        datarow = datarow[:-2] + '\n'
                        colct = len(datarow.split('\t'))
                    if colct == 40:
                        sched_c_file.write(datarow)
                    else:
                        review_file.write(datarow)
                elif rowtype.startswith('SC1/'):
                    while colct < 50:
                        datarow = datarow.replace('\n', '\t\n')
                        colct = len(datarow.split('\t'))
                    while colct > 50 and datarow.endswith('\t\n'):
                        datarow = datarow[:-2] + '\n'
                        colct = len(datarow.split('\t'))
                    if colct == 50:
                        sched_c1_file.write(datarow)
                    else:
                        review_file.write(datarow)
                elif rowtype.startswith('SC2/'):
                    while colct < 19:
                        datarow = datarow.replace('\n', '\t\n')
                        colct = len(datarow.split('\t'))
                    while colct > 19 and datarow.endswith('\t\n'):
                        datarow = datarow[:-2] + '\n'
                        colct = len(datarow.split('\t'))
                    if colct == 19:
                        sched_c2_file.write(datarow)
                    else:
                        review_file.write(datarow)
                elif rowtype.startswith('SD'):
                    while colct < 22:
                        datarow = datarow.replace('\n', '\t\n')
                        colct = len(datarow.split('\t'))
                    while colct > 22 and datarow.endswith('\t\n'):
                        datarow = datarow[:-2] + '\n'
                        colct = len(datarow.split('\t'))
                    if colct == 22:
                        sched_d_file.write(datarow)
                    else:
                        review_file.write(datarow)
                elif rowtype.startswith('SE'):
                    while colct < 46:
                        datarow = datarow.replace('\n', '\t\n')
                        colct = len(datarow.split('\t'))
                    while colct > 46 and datarow.endswith('\t\n'):
                        datarow = datarow[:-2] + '\n'
                        colct = len(datarow.split('\t'))
                    if colct == 46:
                        sched_e_file.write(datarow)
                    else:
                        review_file.write(datarow)
                elif rowtype.startswith('TEXT'):
                    while colct < 8:
                        datarow = datarow.replace('\n', '\t\n')
                        colct = len(datarow.split('\t'))
                    while colct > 8 and datarow.endswith('\t\n'):
                        datarow = datarow[:-2] + '\n'
                        colct = len(datarow.split('\t'))
                    if colct == 8:
                        text_file.write(datarow)
                    else:
                        review_file.write(datarow)
                else:
                    review_file.write(datarow)

            # Move the file to the processed directory
            shutil.move(datafile, destdir + filename)

    except:
        raw_input('An unexpected error has occurred regarding file ' + imageid + '. Press Enter to continue.')
        shutil.move(datafile, reviewdir + filename)
        
finally:
    sched_a_file.close()
    sched_b_file.close()
    sched_c_file.close()
    sched_c1_file.close()
    sched_c2_file.close()
    sched_d_file.close()
    sched_e_file.close()
    text_file.close()
    review_file.close()

    if usedatabaseflag == 0:
        form_f3_file.close()
        form_f3p_file.close()
        form_f3x_file.close()
