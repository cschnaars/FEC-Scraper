/*
FEC database creation scripts:
------------------------------
By Christopher Schnaars, USA Today

In this file, you'll find all the necessary scripts to create an FEC database on SQL Server,
including tables and stored procedures used by the FEC Scraper Python script to interact
with the database.

These scripts were developed on SQL Server 2008 R2 but should work on older versions, including
SQL Server 2000 and 2005. You can use the schema to create similar objects for other
database managers.

Once you create a database (Step 1), you should be able to run the rest of this file as a batch to
create all the tables, stored procedures and triggers at once.

Please note:
None of the tables in this batch is indexed. If you decide to use these tables as the final
resting place for your data rather than as repositories, you probably should create indexes
and keys.

The tables house all fields contained in the FEC data and add three fields:
 * USATID is an IDENTITY column used to give each row a unique ID. This value serves
as a foreign key in child tables that will be created in FECParser.sql. You do not need these
other tables to run FEC Scraper.
 * ImageID is the six digit ID number assigned by the FEC for a particular data file. So, for
example, if you download 421841.fec and add the contents of that file to the database, 421841
will be housed in the ImageID field in this table.
 * Active is a bit field to indicate whether the file is the current file. The default value is 1.
If a report is amended, this field will be set to 0 for all amended reports.

Database triggers (scripted below) control the Active field for you. If you are using a different database
manager, you'll have to come up with logic to handle this field, set it manually or delete data that
has been amended.

The triggers are included here for reference only. The FEC Scraper script does not use them. They
will be used by FEC Parser, however, if you opt to interact with the SQL Server database.

*/



-- Step 1: Create the database
-- Create a new database on your server. These scripts assume you've called the database FEC.
-- If not, modify Step 2 to point to the database you've created.



-- Step 2: Point this file to your database
-- Modify this code to point to your database
USE FEC;
GO



-- Step 3: Create your tables
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

-- This table houses filings by candidates for the House of Representatives
CREATE TABLE [dbo].[Contribs_FormF3](
	[USATID] [int] IDENTITY(1,1) NOT NULL,
	[ImageID] [varchar](9) NOT NULL,
	[Active] [bit] NOT NULL,
	[FormType] [char](4) NOT NULL,
	[CommID] [char](9) NOT NULL,
	[CommName] [varchar](200) NULL,
	[AddressChange] [varchar](1) NULL,
	[CommAddress1] [varchar](34) NULL,
	[CommAddress2] [varchar](34) NULL,
	[CommCity] [varchar](30) NULL,
	[CommState] [varchar](2) NULL,
	[CommZip] [varchar](9) NULL,
	[ElecState] [varchar](2) NULL,
	[ElecDist] [varchar](2) NULL,
	[ReptCode] [varchar](3) NULL,
	[ElecCode] [varchar](5) NULL,
	[strElecDate] [varchar](8) NULL,
	[StateOfElec] [varchar](2) NULL,
	[strCovgFromDate] [varchar](8) NULL,
	[strCovgToDate] [varchar](8) NULL,
	[TreasLastName] [varchar](30) NOT NULL,
	[TreasFirstName] [varchar](20) NOT NULL,
	[TreasMidName] [varchar](20) NULL,
	[TreasPrefix] [varchar](10) NULL,
	[TreasSuffix] [varchar](10) NULL,
	[strDateSigned] [varchar](8) NULL,
	[Line6a_TotalContribs_Prd] [varchar](12) NULL,
	[Line6b_TotalContribRefunds_Prd] [varchar](12) NULL,
	[Line6c_NetContribs_Prd] [varchar](12) NULL,
	[Line7a_TotOpExps_Prd] [varchar](12) NULL,
	[Line7b_TotOffsetToOpExps_Prd] [varchar](12) NULL,
	[Line7c_NetOpExps_Prd] [varchar](12) NULL,
	[Line8_CashOnHandAtClose_Prd] [varchar](12) NULL,
	[Line9_DebtsTo_Prd] [varchar](12) NULL,
	[Line10_DebtsBy_Prd] [varchar](12) NULL,
	[Line11a1_IndivsItemized_Prd] [varchar](12) NULL,
	[Line11a2_IndivsUnitemized_Prd] [varchar](12) NULL,
	[Line11a3_IndivsContribTotal_Prd] [varchar](12) NULL,
	[Line11b_PolPtyComms_Prd] [varchar](12) NULL,
	[Line11c_OtherPACs_Prd] [varchar](12) NULL,
	[Line11d_Candidate_Prd] [varchar](12) NULL,
	[Line11e_TotalContribs_Prd] [varchar](12) NULL,
	[Line12_TransfersFrom_Prd] [varchar](12) NULL,
	[Line13a_LoansByCand_Prd] [varchar](12) NULL,
	[Line13b_OtherLoans_Prd] [varchar](12) NULL,
	[Line13c_TotLoans_Prd] [varchar](12) NULL,
	[Line14_OffsetsToOpExps_Prd] [varchar](12) NULL,
	[Line15_OtherReceipts_Prd] [varchar](12) NULL,
	[Line16_TotReceipts_Prd] [varchar](12) NULL,
	[Line17_OpExps_Prd] [varchar](12) NULL,
	[Line18_TransToOtherComms_Prd] [varchar](12) NULL,
	[Line19a_LoanRepaymts_Cand_Prd] [varchar](12) NULL,
	[Line19b_LoanRepaymts_Other_Prd] [varchar](12) NULL,
	[Line19c_TotLoanRepaymts_Prd] [varchar](12) NULL,
	[Loan20a_IndivRefunds_Prd] [varchar](12) NULL,
	[Line20b_PolPartyCommRefunds_Prd] [varchar](12) NULL,
	[Line20c_OtherPolCommRefunds_Prd] [varchar](12) NULL,
	[Line20d_TotContRefunds_Prd] [varchar](12) NULL,
	[Line21_OtherDisb_Prd] [varchar](12) NULL,
	[Line22_TotDisb_Prd] [varchar](12) NULL,
	[Line23_CashBegin_Prd] [varchar](12) NULL,
	[Line24_TotReceipts_Prd] [varchar](12) NULL,
	[Line25_Subtotal] [varchar](12) NULL,
	[Line26_TotDisbThisPrd_Prd] [varchar](12) NULL,
	[Line27_CashAtClose_Prd] [varchar](12) NULL,
	[Line6a_TotalContribs_Tot] [varchar](12) NULL,
	[Line6b_TotalContribRefunds_Tot] [varchar](12) NULL,
	[Line6c_NetContribs_Tot] [varchar](12) NULL,
	[Line7a_TotOpExps_Tot] [varchar](12) NULL,
	[Line7b_TotOffsetToOpExps_Tot] [varchar](12) NULL,
	[Line7c_NetOpExps_Tot] [varchar](12) NULL,
	[Line11a1_IndivsItemized_Tot] [varchar](12) NULL,
	[Line11a2_IndivsUnitemized_Tot] [varchar](12) NULL,
	[Line11a3_IndivsContribTotal_Tot] [varchar](12) NULL,
	[Line11b_PolPtyComms_Tot] [varchar](12) NULL,
	[Line11c_OtherPACs_Tot] [varchar](12) NULL,
	[Line11d_Candidate_Tot] [varchar](12) NULL,
	[Line11e_TotalContribs_Tot] [varchar](12) NULL,
	[Line12_TransfersFrom_Tot] [varchar](12) NULL,
	[Line13a_LoansByCand_Tot] [varchar](12) NULL,
	[Line13b_OtherLoans_Tot] [varchar](12) NULL,
	[Line13c_TotLoans_Tot] [varchar](12) NULL,
	[Line14_OffsetsToOpExps_Tot] [varchar](12) NULL,
	[Line15_OtherReceipts_Tot] [varchar](12) NULL,
	[Line16_TotReceipts_Tot] [varchar](12) NULL,
	[Line17_OpExps_Tot] [varchar](12) NULL,
	[Line18_TransToOtherComms_Tot] [varchar](12) NULL,
	[Line19a_LoanRepaymts_Cand_Tot] [varchar](12) NULL,
	[Line19b_LoanRepaymts_Other_Tot] [varchar](12) NULL,
	[Line19c_TotLoanRepaymts_Tot] [varchar](12) NULL,
	[Loan20a_IndivRefunds_Tot] [varchar](12) NULL,
	[Line20b_PolPartyCommRefunds_Tot] [varchar](12) NULL,
	[Line20c_OtherPolCommRefunds_Tot] [varchar](12) NULL,
	[Line20d_TotContRefunds_Tot] [varchar](12) NULL,
	[Line21_OtherDisb_Tot] [varchar](12) NULL,
	[Line22_TotDisb_Tot] [varchar](12) NULL
) ON [PRIMARY]
GO

SET ANSI_PADDING OFF
GO

ALTER TABLE [dbo].[Contribs_FormF3] ADD CONSTRAINT [DF_Contribs_FormF3_Active] DEFAULT ((1)) FOR [Active]
GO

SET ANSI_PADDING ON
GO

-- This table houses filings by presidential candidates
CREATE TABLE [dbo].[Contribs_FormF3P](
	[USATID] [int] IDENTITY(1,1) NOT NULL,
	[ImageID] [varchar](9) NOT NULL,
	[Active] [bit] NOT NULL,
	[FormType] [char](4) NOT NULL,
	[CommID] [char](9) NOT NULL,
	[CommName] [varchar](200) NULL,
	[AddressChange] [varchar](1) NULL,
	[CommAddress1] [varchar](34) NULL,
	[CommAddress2] [varchar](34) NULL,
	[CommCity] [varchar](30) NULL,
	[CommState] [varchar](2) NULL,
	[CommZip] [varchar](9) NULL,
	[ActivityPrim] [varchar](1) NULL,
	[ActivityGen] [varchar](1) NULL,
	[ReptCode] [varchar](3) NULL,
	[ElecCode] [varchar](5) NULL,
	[strElecDate] [varchar](8) NULL,
	[ElecState] [varchar](2) NULL,
	[strFromDate] [varchar](8) NULL,
	[strToDate] [varchar](8) NULL,
	[TreasLastName] [varchar](30) NOT NULL,
	[TreasFirstName] [varchar](20) NOT NULL,
	[TreasMidName] [varchar](20) NULL,
	[TreasPrefix] [varchar](10) NULL,
	[TreasSuffix] [varchar](10) NULL,
	[strDateSigned] [char](8) NOT NULL,
	[Line6_CashBegin] [varchar](12) NULL,
	[Line7_TotReceipts] [varchar](12) NULL,
	[Line8_Subtotal] [varchar](12) NULL,
	[Line9_TotalDisb] [varchar](12) NULL,
	[Line10_CashClose] [varchar](12) NULL,
	[Line11_DebtsTo] [varchar](12) NULL,
	[Line12_DebtsBy] [varchar](12) NULL,
	[Line13_ExpendsSubToLimits] [varchar](12) NULL,
	[Line14_NetContribs] [varchar](12) NULL,
	[Line15_NetOpExps] [varchar](12) NULL,
	[Line16_FedFunds_Prd] [varchar](12) NULL,
	[Line17a1_IndivsItemzd_Prd] [varchar](12) NULL,
	[Line17a2_IndivsUnItemzd_Prd] [varchar](12) NULL,
	[Line17a3_IndContTot_Prd] [varchar](12) NULL,
	[Line17b_PolPartyComms_Prd] [varchar](12) NULL,
	[Line17c_OtherPACs_Prd] [varchar](12) NULL,
	[Line17d_Candidate_Prd] [varchar](12) NULL,
	[Line17e_TotContribs_Prd] [varchar](12) NULL,
	[Line18_TransfersFrom_Prd] [varchar](12) NULL,
	[Line19a_CandLoans_Prd] [varchar](12) NULL,
	[Line19b_OtherLoans_Prd] [varchar](12) NULL,
	[Line19c_TotLoans_Prd] [varchar](12) NULL,
	[Line20a_Operating_Prd] [varchar](12) NULL,
	[Line20b_Fundraising_Prd] [varchar](12) NULL,
	[Line20c_LegalAcctg_Prd] [varchar](12) NULL,
	[Line20d_TotExpOffsets_Prd] [varchar](12) NULL,
	[Line21_OtherReceipts_Prd] [varchar](12) NULL,
	[Line22_TotReceipts_Prd] [varchar](12) NULL,
	[Line23_OpExpends_Prd] [varchar](12) NULL,
	[Line24_TransToOtherComms_Prd] [varchar](12) NULL,
	[Line25_FundraisingDisbursed_Prd] [varchar](12) NULL,
	[Line26_ExemptLegalAcctgDisb_Prd] [varchar](12) NULL,
	[Line27a_CandRepymts_Prd] [varchar](12) NULL,
	[Line27b_OtherRepymts_Prd] [varchar](12) NULL,
	[Line27c_TotLoanRepymts_Prd] [varchar](12) NULL,
	[Line28a_IndivRefunds_Prd] [varchar](12) NULL,
	[Line28b_PolPartyCommRefunds_Prd] [varchar](12) NULL,
	[Line28c_OtherPolCommRefunds_Prd] [varchar](12) NULL,
	[Line28d_TotalContRefunds_Prd] [varchar](12) NULL,
	[Line29_OtherDisb_Prd] [varchar](12) NULL,
	[Line30_TotDisb_Prd] [varchar](12) NULL,
	[Line31_ItemsToLiq_Prd] [varchar](12) NULL,
	[AllocAlabama_Prd] [varchar](12) NULL,
	[AllocAlaska_Prd] [varchar](12) NULL,
	[AllocArizona_Prd] [varchar](12) NULL,
	[AllocArkansas_Prd] [varchar](12) NULL,
	[AllocCalifornia_Prd] [varchar](12) NULL,
	[AllocColorado_Prd] [varchar](12) NULL,
	[AllocConnecticut_Prd] [varchar](12) NULL,
	[AllocDelaware_Prd] [varchar](12) NULL,
	[AllocDistCol_Prd] [varchar](12) NULL,
	[AllocFlorida_Prd] [varchar](12) NULL,
	[AllocGeorgia_Prd] [varchar](12) NULL,
	[AllocHawaii_Prd] [varchar](12) NULL,
	[AllocIdaho_Prd] [varchar](12) NULL,
	[AllocIllinois_Prd] [varchar](12) NULL,
	[AllocIndiana_Prd] [varchar](12) NULL,
	[AllocIowa_Prd] [varchar](12) NULL,
	[AllocKansas_Prd] [varchar](12) NULL,
	[AllocKentucky_Prd] [varchar](12) NULL,
	[AllocLouisiana_Prd] [varchar](12) NULL,
	[AllocMaine_Prd] [varchar](12) NULL,
	[AllocMaryland_Prd] [varchar](12) NULL,
	[AllocMassachusetts_Prd] [varchar](12) NULL,
	[AllocMichigan_Prd] [varchar](12) NULL,
	[AllocMinnesota_Prd] [varchar](12) NULL,
	[AllocMississippi_Prd] [varchar](12) NULL,
	[AllocMissouri_Prd] [varchar](12) NULL,
	[AllocMontana_Prd] [varchar](12) NULL,
	[AllocNebraska_Prd] [varchar](12) NULL,
	[AllocNevada_Prd] [varchar](12) NULL,
	[AllocNewHampshire_Prd] [varchar](12) NULL,
	[AllocNewJersey_Prd] [varchar](12) NULL,
	[AllocNewMexico_Prd] [varchar](12) NULL,
	[AllocNewYork_Prd] [varchar](12) NULL,
	[AllocNorthCarolina_Prd] [varchar](12) NULL,
	[AllocNorthDakota_Prd] [varchar](12) NULL,
	[AllocOhio_Prd] [varchar](12) NULL,
	[AllocOklahoma_Prd] [varchar](12) NULL,
	[AllocOregon_Prd] [varchar](12) NULL,
	[AllocPennsylvania_Prd] [varchar](12) NULL,
	[AllocRhodeIsland_Prd] [varchar](12) NULL,
	[AllocSouthCarolina_Prd] [varchar](12) NULL,
	[AllocSouthDakota_Prd] [varchar](12) NULL,
	[AllocTennessee_Prd] [varchar](12) NULL,
	[AllocTexas_Prd] [varchar](12) NULL,
	[AllocUtah_Prd] [varchar](12) NULL,
	[AllocVermont_Prd] [varchar](12) NULL,
	[AllocVirginia_Prd] [varchar](12) NULL,
	[AllocWashington_Prd] [varchar](12) NULL,
	[AllocWestVirginia_Prd] [varchar](12) NULL,
	[AllocWisconsin_Prd] [varchar](12) NULL,
	[AllocWyoming_Prd] [varchar](12) NULL,
	[AllocPuertoRico_Prd] [varchar](12) NULL,
	[AllocGuam_Prd] [varchar](12) NULL,
	[AllocVirginIslands_Prd] [varchar](12) NULL,
	[AllocStatesTotal_Prd] [varchar](12) NULL,
	[Line16_FedFunds_Tot] [varchar](12) NULL,
	[Line17a1_IndivsItemzd_Tot] [varchar](12) NULL,
	[Line17a2_IndivsUnItemzd_Tot] [varchar](12) NULL,
	[Line17a3_IndContTot_Tot] [varchar](12) NULL,
	[Line17b_PolPartyComms_Tot] [varchar](12) NULL,
	[Line17c_OtherPACs_Tot] [varchar](12) NULL,
	[Line17d_Candidate_Tot] [varchar](12) NULL,
	[Line17e_TotContribs_Tot] [varchar](12) NULL,
	[Line18_TransfersFrom_Tot] [varchar](12) NULL,
	[Line19a_CandLoans_Tot] [varchar](12) NULL,
	[Line19b_OtherLoans_Tot] [varchar](12) NULL,
	[Line19c_TotLoans_Tot] [varchar](12) NULL,
	[Line20a_Operating_Tot] [varchar](12) NULL,
	[Line20b_Fundraising_Tot] [varchar](12) NULL,
	[Line20c_LegalAcctg_Tot] [varchar](12) NULL,
	[Line20d_TotExpOffsets_Tot] [varchar](12) NULL,
	[Line21_OtherReceipts_Tot] [varchar](12) NULL,
	[Line22_TotReceipts_Tot] [varchar](12) NULL,
	[Line23_OpExpends_Tot] [varchar](12) NULL,
	[Line24_TransToOtherComms_Tot] [varchar](12) NULL,
	[Line25_FundraisingDisbursed_Tot] [varchar](12) NULL,
	[Line26_ExemptLegalAcctgDisb_Tot] [varchar](12) NULL,
	[Line27a_CandRepymts_Tot] [varchar](12) NULL,
	[Line27b_OtherRepymts_Tot] [varchar](12) NULL,
	[Line27c_TotLoanRepymts_Tot] [varchar](12) NULL,
	[Line28a_IndivRefunds_Tot] [varchar](12) NULL,
	[Line28b_PolPartyCommRefunds_Tot] [varchar](12) NULL,
	[Line28c_OtherPolCommRefunds_Tot] [varchar](12) NULL,
	[Line28d_TotalContRefunds_Tot] [varchar](12) NULL,
	[Line29_OtherDisb_Tot] [varchar](12) NULL,
	[Line30_TotDisb_Tot] [varchar](12) NULL,
	[AllocAlabama_Tot] [varchar](12) NULL,
	[AllocAlaska_Tot] [varchar](12) NULL,
	[AllocArizona_Tot] [varchar](12) NULL,
	[AllocArkansas_Tot] [varchar](12) NULL,
	[AllocCalifornia_Tot] [varchar](12) NULL,
	[AllocColorado_Tot] [varchar](12) NULL,
	[AllocConnecticut_Tot] [varchar](12) NULL,
	[AllocDelaware_Tot] [varchar](12) NULL,
	[AllocDistCol_Tot] [varchar](12) NULL,
	[AllocFlorida_Tot] [varchar](12) NULL,
	[AllocGeorgia_Tot] [varchar](12) NULL,
	[AllocHawaii_Tot] [varchar](12) NULL,
	[AllocIdaho_Tot] [varchar](12) NULL,
	[AllocIllinois_Tot] [varchar](12) NULL,
	[AllocIndiana_Tot] [varchar](12) NULL,
	[AllocIowa_Tot] [varchar](12) NULL,
	[AllocKansas_Tot] [varchar](12) NULL,
	[AllocKentucky_Tot] [varchar](12) NULL,
	[AllocLouisiana_Tot] [varchar](12) NULL,
	[AllocMaine_Tot] [varchar](12) NULL,
	[AllocMaryland_Tot] [varchar](12) NULL,
	[AllocMassachusetts_Tot] [varchar](12) NULL,
	[AllocMichigan_Tot] [varchar](12) NULL,
	[AllocMinnesota_Tot] [varchar](12) NULL,
	[AllocMississippi_Tot] [varchar](12) NULL,
	[AllocMissouri_Tot] [varchar](12) NULL,
	[AllocMontana_Tot] [varchar](12) NULL,
	[AllocNebraska_Tot] [varchar](12) NULL,
	[AllocNevada_Tot] [varchar](12) NULL,
	[AllocNewHampshire_Tot] [varchar](12) NULL,
	[AllocNewJersey_Tot] [varchar](12) NULL,
	[AllocNewMexico_Tot] [varchar](12) NULL,
	[AllocNewYork_Tot] [varchar](12) NULL,
	[AllocNorthCarolina_Tot] [varchar](12) NULL,
	[AllocNorthDakota_Tot] [varchar](12) NULL,
	[AllocOhio_Tot] [varchar](12) NULL,
	[AllocOklahoma_Tot] [varchar](12) NULL,
	[AllocOregon_Tot] [varchar](12) NULL,
	[AllocPennsylvania_Tot] [varchar](12) NULL,
	[AllocRhodeIsland_Tot] [varchar](12) NULL,
	[AllocSouthCarolina_Tot] [varchar](12) NULL,
	[AllocSouthDakota_Tot] [varchar](12) NULL,
	[AllocTennessee_Tot] [varchar](12) NULL,
	[AllocTexas_Tot] [varchar](12) NULL,
	[AllocUtah_Tot] [varchar](12) NULL,
	[AllocVermont_Tot] [varchar](12) NULL,
	[AllocVirginia_Tot] [varchar](12) NULL,
	[AllocWashington_Tot] [varchar](12) NULL,
	[AllocWestVirginia_Tot] [varchar](12) NULL,
	[AllocWisconsin_Tot] [varchar](12) NULL,
	[AllocWyoming_Tot] [varchar](12) NULL,
	[AllocPuertoRico_Tot] [varchar](12) NULL,
	[AllocGuam_Tot] [varchar](12) NULL,
	[AllocVirginIslands_Tot] [varchar](12) NULL,
	[AllocStatesTotal_Tot] [varchar](12) NULL
) ON [PRIMARY]
GO

SET ANSI_PADDING OFF
GO

ALTER TABLE [dbo].[Contribs_FormF3P] ADD  CONSTRAINT [DF_Contribs_FormF3P_Active] DEFAULT ((1)) FOR [Active]
GO

SET ANSI_PADDING ON
GO

-- This table houses filings by PACs and other organizations
CREATE TABLE [dbo].[Contribs_FormF3X](
	[USATID] [int] IDENTITY(1,1) NOT NULL,
	[ImageID] [varchar](9) NOT NULL,
	[Active] [bit] NOT NULL,
	[FormType] [char](4) NOT NULL,
	[CommID] [char](9) NOT NULL,
	[CommName] [varchar](200) NULL,
	[AddressChange] [varchar](1) NULL,
	[CommAddress1] [varchar](34) NULL,
	[CommAddress2] [varchar](34) NULL,
	[CommCity] [varchar](30) NULL,
	[CommState] [varchar](2) NULL,
	[CommZip] [varchar](9) NULL,
	[ReptCode] [varchar](3) NULL,
	[ElecCode] [varchar](5) NULL,
	[strElecDate] [varchar](8) NULL,
	[ElecState] [varchar](2) NULL,
	[strFromDate] [varchar](8) NULL,
	[strToDate] [varchar](8) NULL,
	[flgQualifiedComm] [varchar](1) NULL,
	[TreasLastName] [varchar](30) NOT NULL,
	[TreasFirstName] [varchar](20) NOT NULL,
	[TreasMidName] [varchar](20) NULL,
	[TreasPrefix] [varchar](10) NULL,
	[TreasSuffix] [varchar](10) NULL,
	[strDateSigned] [char](8) NOT NULL,
	[Line6b_CashBegin_Prd] [varchar](12) NULL,
	[Line6c_TotalRects_Prd] [varchar](12) NULL,
	[Line6d_CashBeginSubtotal_Prd] [varchar](12) NULL,
	[Line7_TotDisbmts_Prd] [varchar](12) NULL,
	[Line8_CashOnHandAtClose_Prd] [varchar](12) NULL,
	[Line9_DebtsTo_Prd] [varchar](12) NULL,
	[Line10_DebtsBy_Prd] [varchar](12) NULL,
	[Line11a1_Itemized_Prd] [varchar](12) NULL,
	[Line11a2_Unitemized_Prd] [varchar](12) NULL,
	[Line11a3_Total_Prd] [varchar](12) NULL,
	[Line11b_PolPtyComms_Prd] [varchar](12) NULL,
	[Line11c_OtherPACs_Prd] [varchar](12) NULL,
	[Line11d_TotalContribs_Prd] [varchar](12) NULL,
	[Line12_TransfersFrom_Prd] [varchar](12) NULL,
	[Line13_AllLoansRcvd_Prd] [varchar](12) NULL,
	[Line14_LoanRepymtsRecv_Prd] [varchar](12) NULL,
	[Line15_OffsetsToOpExps_Refunds_Prd] [varchar](12) NULL,
	[Line16_RefundsOfFedContribs_Prd] [varchar](12) NULL,
	[Line17_OtherFedRects_Divds_Prd] [varchar](12) NULL,
	[Line18a_TransfersFromNonFedAcct_H3_Prd] [varchar](12) NULL,
	[Line18b_TransfersFromNonFed_LevinH5_Prd] [varchar](12) NULL,
	[Line18c_TotalNonFedTransfers_Prd] [varchar](12) NULL,
	[Line19_TotalReceipts_Prd] [varchar](12) NULL,
	[Line20_TotalFedReceipts_Prd] [varchar](12) NULL,
	[Line21a1_FedShare_Prd] [varchar](12) NULL,
	[Line21a2_NonFedShare_Prd] [varchar](12) NULL,
	[Line21b_OtherFedOpExps_Prd] [varchar](12) NULL,
	[Line21c_TotOpExps_Prd] [varchar](12) NULL,
	[Line22_TransToOtherComms_Prd] [varchar](12) NULL,
	[Line23_ContribsToFedCandsOrComms_Prd] [varchar](12) NULL,
	[Line24_IndptExps_Prd] [varchar](12) NULL,
	[Line25_CoordtdExpByPrtyComms_Prd] [varchar](12) NULL,
	[Line26_LoanRepayments_Prd] [varchar](12) NULL,
	[Line27_LoansMade_Prd] [varchar](12) NULL,
	[Line28a_IndivRefunds_Prd] [varchar](12) NULL,
	[Line28b_PolPartyCommRefunds_Prd] [varchar](12) NULL,
	[Line28c_OtherPolCommRefunds_Prd] [varchar](12) NULL,
	[Line28d_TotalContRefunds_Prd] [varchar](12) NULL,
	[Line29_OtherDisb_Prd] [varchar](12) NULL,
	[Line30a1_SharedFedActH6FedShare_Prd] [varchar](12) NULL,
	[Line30a2_SharedFedActH6NonFed_Prd] [varchar](12) NULL,
	[Line30b_NonAlloc100PctFedElecActivity_Prd] [varchar](12) NULL,
	[Line30c_TotFedElecActivity_Prd] [varchar](12) NULL,
	[Line31_TotDisbmts_Prd] [varchar](12) NULL,
	[Line32_TotFedDisbmts_Prd] [varchar](12) NULL,
	[Line33_TotContribs_Prd] [varchar](12) NULL,
	[Line34_TotContribRefunds_Prd] [varchar](12) NULL,
	[Line35_NetContribs_Prd] [varchar](12) NULL,
	[Line36_TotFedOpExps_Prd] [varchar](12) NULL,
	[Line37_OffsetsToOpExps_Prd] [varchar](12) NULL,
	[Line38_NetOpExps_Prd] [varchar](12) NULL,
	[Line6b_CashBegin_Tot] [varchar](12) NULL,
	[Line6b_Year] [varchar](12) NULL,
	[Line6c_TotalRects_Tot] [varchar](12) NULL,
	[Line6d_CashBeginSubtotal_Tot] [varchar](12) NULL,
	[Line7_TotDisbmts_Tot] [varchar](12) NULL,
	[Line8_CashOnHandAtClose_Tot] [varchar](12) NULL,
	[Line11a1_Itemized_Tot] [varchar](12) NULL,
	[Line11a2_Unitemized_Tot] [varchar](12) NULL,
	[Line11a3_Total_Tot] [varchar](12) NULL,
	[Line11b_PolPtyComms_Tot] [varchar](12) NULL,
	[Line11c_OtherPACs_Tot] [varchar](12) NULL,
	[Line11d_TotalContribs_Tot] [varchar](12) NULL,
	[Line12_TransfersFrom_Tot] [varchar](12) NULL,
	[Line13_AllLoansRcvd_Tot] [varchar](12) NULL,
	[Line14_LoanRepymtsRecv_Tot] [varchar](12) NULL,
	[Line15_OffsetsToOpExps_Refunds_Tot] [varchar](12) NULL,
	[Line16_RefundsOfFedContribs_Tot] [varchar](12) NULL,
	[Line17_OtherFedRects_Divds_Tot] [varchar](12) NULL,
	[Line18a_TransfersFromNonFedAcct_H3_Tot] [varchar](12) NULL,
	[Line18b_TransfersFromNonFed_LevinH5_Tot] [varchar](12) NULL,
	[Line18c_TotalNonFedTransfers_Tot] [varchar](12) NULL,
	[Line19_TotalReceipts_Tot] [varchar](12) NULL,
	[Line20_TotalFedReceipts_Tot] [varchar](12) NULL,
	[Line21a1_FedShare_Tot] [varchar](12) NULL,
	[Line21a2_NonFedShare_Tot] [varchar](12) NULL,
	[Line21b_OtherFedOpExps_Tot] [varchar](12) NULL,
	[Line21c_TotOpExps_Tot] [varchar](12) NULL,
	[Line22_TransToOtherComms_Tot] [varchar](12) NULL,
	[Line23_ContribsToFedCandsOrComms_Tot] [varchar](12) NULL,
	[Line24_IndptExps_Tot] [varchar](12) NULL,
	[Line25_CoordtdExpByPrtyComms_Tot] [varchar](12) NULL,
	[Line26_LoanRepayments_Tot] [varchar](12) NULL,
	[Line27_LoansMade_Tot] [varchar](12) NULL,
	[Line28a_IndivRefunds_Tot] [varchar](12) NULL,
	[Line28b_PolPartyCommRefunds_Tot] [varchar](12) NULL,
	[Line28c_OtherPolCommRefunds_Tot] [varchar](12) NULL,
	[Line28d_TotalContRefunds_Tot] [varchar](12) NULL,
	[Line29_OtherDisb_Tot] [varchar](12) NULL,
	[Line30a1_SharedFedActH6FedShare_Tot] [varchar](12) NULL,
	[Line30a2_SharedFedActH6NonFed_Tot] [varchar](12) NULL,
	[Line30b_NonAlloc100PctFedElecActivity_Tot] [varchar](12) NULL,
	[Line30c_TotFedElecActivity_Tot] [varchar](12) NULL,
	[Line31_TotDisbmts_Tot] [varchar](12) NULL,
	[Line32_TotFedDisbmts_Tot] [varchar](12) NULL,
	[Line33_TotContribs_Tot] [varchar](12) NULL,
	[Line34_TotContribRefunds_Tot] [varchar](12) NULL,
	[Line35_NetContribs_Tot] [varchar](12) NULL,
	[Line36_TotFedOpExps_Tot] [varchar](12) NULL,
	[Line37_OffsetsToOpExps_Tot] [varchar](12) NULL,
	[Line38_NetOpExps_Tot] [varchar](12) NULL
) ON [PRIMARY]
GO

SET ANSI_PADDING OFF
GO

ALTER TABLE [dbo].[Contribs_FormF3X] ADD  CONSTRAINT [DF_Contribs_FormF3X_Active] DEFAULT ((1)) FOR [Active]
GO



-- Step 4: Create triggers
-- Triggers are used to track when a report is amended. The active field is set to 1 for the current
-- report and 0 for amended reports.
CREATE TRIGGER [dbo].[UpdateF3Active] ON [dbo].[Contribs_FormF3]
AFTER INSERT

AS

BEGIN
	SET NOCOUNT ON;

	UPDATE a
	SET a.Active = 0
	FROM Contribs_FormF3 a
	INNER JOIN Contribs_FormF3 b
		ON a.CommID = b.CommID
			AND a.ImageID < b.ImageID
			AND a.Active = 1
			AND b.Active = 1
			AND a.ReptCode = b.ReptCode
			AND a.strCovgFromDate = b.strCovgFromDate
			AND a.strCovgToDate = b.strCovgToDate;

END
GO



CREATE TRIGGER [dbo].[UpdateF3PActive] ON [dbo].[Contribs_FormF3P]
AFTER INSERT

AS

BEGIN
	SET NOCOUNT ON;

	UPDATE a
	SET a.Active = 0
	FROM Contribs_FormF3P a
	INNER JOIN Contribs_FormF3P b
		ON a.CommID = b.CommID
			AND a.ImageID < b.ImageID
			AND a.Active = 1
			AND b.Active = 1
			AND a.ReptCode = b.ReptCode
			AND a.strFromDate = b.strFromDate
			AND a.strToDate = b.strToDate;

END
GO



CREATE TRIGGER [dbo].[UpdateF3XActive] ON [dbo].[Contribs_FormF3X]
AFTER INSERT

AS

BEGIN
	SET NOCOUNT ON;

	UPDATE a
	SET a.Active = 0
	FROM Contribs_FormF3X a
	INNER JOIN Contribs_FormF3X b
		ON a.CommID = b.CommID
			AND a.ImageID < b.ImageID
			AND a.Active = 1
			AND b.Active = 1
			AND a.ReptCode = b.ReptCode
			AND a.strFromDate = b.strFromDate
			AND a.strToDate = b.strToDate;

END
GO



-- Step 5: Create your stored procedures
-- These stored procedures are called by the FEC Scraper Python script to determine
-- previously downloaded committees and files.
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- This stored procedure retrieves Committee IDs that already exist in the database
CREATE PROC [dbo].[usp_GetCommitteeIDs]

AS

SELECT CommID
FROM Contribs_FormF3
UNION
SELECT CommID
FROM Contribs_FormF3P
UNION
SELECT CommID
FROM Contribs_FormF3X
GROUP BY CommID;
GO



-- This stored procedure retrieves file IDs that already exist in the database
CREATE PROC [dbo].[usp_GetFileIDs]

AS

SELECT ImageID
FROM Contribs_FormF3
UNION
SELECT ImageID
FROM Contribs_FormF3P
UNION
SELECT ImageID
FROM Contribs_FormF3X;

GO

