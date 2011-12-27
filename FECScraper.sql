/*
FEC database creation scripts:
------------------------------
By Christopher Schnaars, USA Today

In this file, you'll find all the necessary scripts to create an FEC database on SQL Server,
including tables and stored procedures used by the FEC Scraper and FEC Parser Python scripts
to interact with the database.

These scripts were developed on SQL Server 2008 R2 but should work on older versions, including
SQL Server 2000 and 2005. You can use the schema to create similar objects for other
database managers.

Once you create a database (Step 1), you should be able to run the rest of this file as a batch to
create all the tables, stored procedures and triggers at once.

Please note:
None of the tables in this batch is indexed. If you decide to use these tables as the final
resting place for your data rather than as repositories, you probably should create indexes
and keys.

The tables house all fields contained in the FEC data and add two fields:
 * ImageID is the six digit ID number assigned by the FEC for a particular data file. So, for
example, if you download 421841.fec and add the contents of that file to the database, 421841
will be housed in the ImageID field in this table.
 * Active is a bit field to indicate whether the file is the current file. The default value is 1.
If a report is amended, this field will be set to 0 for all amended reports.

Database triggers (scripted below) control the Active field for you. If you use a different database
manager, you'll have to come up with logic to handle this field, set it manually or delete data that
has been amended.

*/



-- Step 1: Create the database
-- Create a new database on your server. These scripts assume you've called the database FEC.
-- If not, modify Step 2 to point to the database you've created.



-- Step 2: Point this file to your database
-- Modify this code to point to your database
USE FEC;
GO



-- Step 3: Create header tables
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

-- This table houses filings by candidates for the House of Representatives
CREATE TABLE [dbo].[Contribs_FormF3](
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
	[Line22_TotDisb_Tot] [varchar](12) NULL,
 CONSTRAINT [PK_Contribs_FormF3] PRIMARY KEY CLUSTERED 
(
	[ImageID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
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
	[AllocStatesTotal_Tot] [varchar](12) NULL,
 CONSTRAINT [PK_Contribs_FormF3P] PRIMARY KEY CLUSTERED 
(
	[ImageID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

SET ANSI_PADDING OFF
GO

ALTER TABLE [dbo].[Contribs_FormF3P] ADD CONSTRAINT [DF_Contribs_FormF3P_Active] DEFAULT ((1)) FOR [Active]
GO

SET ANSI_PADDING ON
GO

-- This table houses filings by PACs and other organizations
CREATE TABLE [dbo].[Contribs_FormF3X](
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
	[Line38_NetOpExps_Tot] [varchar](12) NULL,
 CONSTRAINT [PK_Contribs_FormF3X] PRIMARY KEY CLUSTERED 
(
	[ImageID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

SET ANSI_PADDING OFF
GO

ALTER TABLE [dbo].[Contribs_FormF3X] ADD CONSTRAINT [DF_Contribs_FormF3X_Active] DEFAULT ((1)) FOR [Active]
GO



-- Step 4: Create child tables
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

-- Schedule A:
CREATE TABLE [dbo].[Contribs_SchedA](
	[USATID] [int] IDENTITY(1,1) NOT NULL,
	[ParentType] [varchar](5) NOT NULL,
	[ImageID] [int] NOT NULL,
	[FormType] [varchar](8) NOT NULL,
	[CommID] [char](9) NOT NULL,
	[TransID] [varchar](20) NOT NULL,
	[BackRefTransID] [varchar](20) NULL,
	[BackRefSchedName] [varchar](8) NULL,
	[EntityType] [char](3) NOT NULL,
	[ContOrgName] [varchar](200) NULL,
	[ContLastName] [varchar](30) NULL,
	[ContFirstName] [varchar](20) NULL,
	[ContMidName] [varchar](20) NULL,
	[ContPrefix] [varchar](10) NULL,
	[ContSuffix] [varchar](10) NULL,
	[ContAddress1] [varchar](34) NULL,
	[ContAddress2] [varchar](34) NULL,
	[ContCity] [varchar](30) NULL,
	[ContState] [varchar](2) NULL,
	[ContZip] [varchar](9) NULL,
	[ElecCode] [varchar](5) NULL,
	[ElecOtherDesc] [varchar](20) NULL,
	[strContDate] [varchar](8) NULL,
	[ContAmount] [varchar](12) NULL,
	[ContAggregate] [varchar](12) NULL,
	[ContPurposeCode] [varchar](3) NULL,
	[ContPurposeDesc] [varchar](100) NULL,
	[ContEmployer] [varchar](38) NULL,
	[ContOccupation] [varchar](38) NULL,
	[DonorCommFECID] [varchar](9) NULL,
	[DonorCommName] [varchar](200) NULL,
	[DonorCandFECID] [varchar](9) NULL,
	[DonorCandLastName] [varchar](30) NULL,
	[DonorCandFirstName] [varchar](20) NULL,
	[DonorCandMidName] [varchar](20) NULL,
	[DonorCandPrefix] [varchar](10) NULL,
	[DonorCandSuffix] [varchar](10) NULL,
	[DonorCandOffice] [varchar](1) NULL,
	[DonorCandState] [varchar](2) NULL,
	[DonorCandDist] [varchar](2) NULL,
	[ConduitName] [varchar](200) NULL,
	[ConduitAddress1] [varchar](34) NULL,
	[ConduitAddress2] [varchar](34) NULL,
	[ConduitCity] [varchar](30) NULL,
	[ConduitState] [varchar](2) NULL,
	[ConduitZip] [varchar](9) NULL,
	[MemoCode] [varchar](1) NULL,
	[MemoText] [varchar](100) NULL
) ON [PRIMARY]
GO

-- Schedule B:
CREATE TABLE [dbo].[Contribs_SchedB](
	[USATID] [int] IDENTITY(1,1) NOT NULL,
	[ParentType] [varchar](5) NOT NULL,
	[ImageID] [int] NOT NULL,
	[FormType] [varchar](8) NOT NULL,
	[FilerCommID] [char](9) NOT NULL,
	[TransID] [varchar](20) NOT NULL,
	[BackRefTransID] [varchar](20) NULL,
	[BackRefSchedName] [varchar](8) NULL,
	[EntityType] [varchar](3) NULL,
	[PayeeOrgName] [varchar](200) NULL,
	[PayeeLastName] [varchar](30) NULL,
	[PayeeFirstName] [varchar](20) NULL,
	[PayeeMidName] [varchar](20) NULL,
	[PayeePrefix] [varchar](10) NULL,
	[PayeeSuffix] [varchar](10) NULL,
	[PayeeAddress1] [varchar](34) NULL,
	[PayeeAddress2] [varchar](34) NULL,
	[PayeeCity] [varchar](30) NULL,
	[PayeeState] [varchar](2) NULL,
	[PayeeZip] [varchar](9) NULL,
	[ElecCode] [varchar](5) NULL,
	[ElecOtherDesc] [varchar](20) NULL,
	[strExpDate] [varchar](8) NULL,
	[ExpAmount] [varchar](12) NULL,
	[SemiAnnRefundedBundledAmt] [varchar](12) NULL,
	[ExpPurpCode] [varchar](3) NULL,
	[ExpPurpDesc] [varchar](100) NULL,
	[CatCode] [varchar](3) NULL,
	[BenCommFECID] [varchar](9) NULL,
	[BenCommName] [varchar](200) NULL,
	[BenCandFECID] [varchar](9) NULL,
	[BenCandLastName] [varchar](30) NULL,
	[BenCandFirstName] [varchar](20) NULL,
	[BenCandMidName] [varchar](20) NULL,
	[BenCandPrefix] [varchar](10) NULL,
	[BenCandSuffix] [varchar](10) NULL,
	[BenCandOffice] [varchar](1) NULL,
	[BenCandState] [varchar](2) NULL,
	[BenCandDist] [varchar](2) NULL,
	[ConduitName] [varchar](200) NULL,
	[ConduitAddress1] [varchar](34) NULL,
	[ConduitAddress2] [varchar](34) NULL,
	[ConduitCity] [varchar](30) NULL,
	[ConduitState] [varchar](2) NULL,
	[ConduitZip] [varchar](9) NULL,
	[MemoCode] [varchar](1) NULL,
	[MemoText] [varchar](100) NULL
) ON [PRIMARY]

GO

-- Schedule C:
CREATE TABLE [dbo].[Contribs_SchedC](
	[USATID] [int] IDENTITY(1,1) NOT NULL,
	[ParentType] [varchar](5) NOT NULL,
	[ImageID] [int] NOT NULL,
	[FormType] [varchar](8) NOT NULL,
	[FilerCommID] [char](9) NOT NULL,
	[TransID] [varchar](20) NOT NULL,
	[RectLineNbr] [varchar](8) NULL,
	[EntityType] [varchar](3) NULL,
	[LenderOrgName] [varchar](200) NULL,
	[LenderLastName] [varchar](30) NULL,
	[LenderFirstName] [varchar](20) NULL,
	[LenderMidName] [varchar](20) NULL,
	[LenderPrefix] [varchar](10) NULL,
	[LenderSuffix] [varchar](10) NULL,
	[LenderAddress1] [varchar](34) NULL,
	[LenderAddress2] [varchar](34) NULL,
	[LenderCity] [varchar](30) NULL,
	[LenterState] [varchar](2) NULL,
	[LenderZip] [varchar](9) NULL,
	[ElecCod] [varchar](5) NULL,
	[ElecOtherDesc] [varchar](20) NULL,
	[LoanAmt] [varchar](12) NULL,
	[LoanPymtToDate] [varchar](12) NULL,
	[LoanBal] [varchar](12) NULL,
	[strLoanIncurredDate] [varchar](8) NULL,
	[strLoanDueDate] [varchar](15) NULL,
	[LoanIntRate] [varchar](15) NULL,
	[LoanSecuredFlag] [varchar](1) NULL,
	[LoanPersFundsFlag] [varchar](1) NULL,
	[LenderCommID] [varchar](9) NULL,
	[LenderCandID] [varchar](9) NULL,
	[LenderCandLastName] [varchar](30) NULL,
	[LenderCandFirstName] [varchar](20) NULL,
	[LenderCandMidName] [varchar](20) NULL,
	[LenderCandPrefix] [varchar](10) NULL,
	[LenderCandSuffix] [varchar](10) NULL,
	[LenderCandOffice] [varchar](1) NULL,
	[LenderCandState] [varchar](2) NULL,
	[LenderCandDist] [varchar](2) NULL,
	[MemoCode] [varchar](1) NULL,
	[MemoText] [varchar](100) NULL
) ON [PRIMARY]
GO

-- Schedule C1:
CREATE TABLE [dbo].[Contribs_SchedC1](
	[USATID] [int] IDENTITY(1,1) NOT NULL,
	[ParentType] [varchar](5) NOT NULL,
	[ImageID] [int] NOT NULL,
	[FormType] [varchar](8) NOT NULL,
	[FilerCommID] [char](9) NOT NULL,
	[TransID] [varchar](20) NOT NULL,
	[BackRefTransID] [varchar](20) NOT NULL,
	[LenderOrgName] [varchar](200) NULL,
	[LenderAddress1] [varchar](34) NULL,
	[LenderAddress2] [varchar](34) NULL,
	[LenderCity] [varchar](30) NULL,
	[LenderState] [varchar](2) NULL,
	[LenderZip] [varchar](9) NULL,
	[LoanAmt] [varchar](12) NULL,
	[LoanIntRate] [varchar](15) NULL,
	[strLoanIncurredDate] [varchar](8) NULL,
	[strLoanDueDate] [varchar](15) NULL,
	[A1_LoanRestructuredFlag] [varchar](1) NULL,
	[A2_strOrigLoanIncurredDate] [varchar](8) NULL,
	[B1_CreditAmtThisDraw] [varchar](12) NULL,
	[B2_TotBalance] [varchar](12) NULL,
	[C_OthersLiableFlag] [varchar](1) NULL,
	[D_CollateralFlag] [varchar](1) NULL,
	[D1_CollateralDescription] [varchar](100) NULL,
	[D2_CollateralValue] [varchar](12) NULL,
	[D3_PerfectedInterestFlag] [varchar](1) NULL,
	[E1_FutureIncomeFlag] [varchar](1) NULL,
	[E2_FutureIncomeDesc] [varchar](100) NULL,
	[E3_EstimatedValue] [varchar](12) NULL,
	[E4_strDepositoryAcctEstablishedDate] [varchar](8) NULL,
	[E5_AcctLocName] [varchar](200) NULL,
	[E6_AcctAddress1] [varchar](34) NULL,
	[E7_AcctAddress1] [varchar](34) NULL,
	[E8_AcctCity] [varchar](30) NULL,
	[E9_State] [varchar](2) NULL,
	[E10_Zip] [varchar](9) NULL,
	[E11_strDepositAcctAuthDate] [varchar](8) NULL,
	[F_LoanBasisDesc] [varchar](100) NULL,
	[G_TreasLastName] [varchar](30) NULL,
	[G_TreasFirstName] [varchar](20) NULL,
	[G_TreasMidName] [varchar](20) NULL,
	[G_TreasPrefix] [varchar](10) NULL,
	[G_TreasSuffix] [varchar](10) NULL,
	[G_strDateSigned] [varchar](8) NULL,
	[H_AuthorizedLastName] [varchar](30) NULL,
	[H_AuthorizedfirstName] [varchar](20) NULL,
	[H_AuthorizedMidName] [varchar](20) NULL,
	[H_AuthorizedPrefix] [varchar](10) NULL,
	[H_AuthorizedSuffix] [varchar](10) NULL,
	[H_AuthorizedTitle] [varchar](20) NULL,
	[H_strDateSigned] [varchar](8) NULL
) ON [PRIMARY]
GO

-- Schedule C2:
CREATE TABLE [dbo].[Contribs_SchedC2](
	[USATID] [int] IDENTITY(1,1) NOT NULL,
	[ParentType] [varchar](5) NOT NULL,
	[ImageID] [int] NOT NULL,
	[FormType] [varchar](8) NOT NULL,
	[FilerCommID] [char](9) NOT NULL,
	[TransID] [varchar](20) NOT NULL,
	[BackRefTransID] [varchar](20) NOT NULL,
	[GuarLastName] [varchar](30) NOT NULL,
	[GuarFirstName] [varchar](20) NOT NULL,
	[GuarMidName] [varchar](20) NULL,
	[GuarPrefix] [varchar](10) NULL,
	[GuarSuffix] [varchar](10) NULL,
	[GuarAddress1] [varchar](34) NULL,
	[GuarAddress2] [varchar](34) NULL,
	[GuarCity] [varchar](30) NULL,
	[GuarState] [varchar](2) NULL,
	[GuarZip] [varchar](9) NULL,
	[GuarEmployer] [varchar](38) NULL,
	[GuarOccupation] [varchar](38) NULL,
	[GuarAmt] [varchar](12) NULL
) ON [PRIMARY]
GO

-- Schedule D:
CREATE TABLE [dbo].[Contribs_SchedD](
	[USATID] [int] IDENTITY(1,1) NOT NULL,
	[ParentType] [varchar](5) NOT NULL,
	[ImageID] [int] NOT NULL,
	[FormType] [varchar](8) NOT NULL,
	[CommID] [char](9) NOT NULL,
	[TransID] [varchar](20) NOT NULL,
	[EntityType] [varchar](3) NOT NULL,
	[CredOrgName] [varchar](200) NULL,
	[CredLastName] [varchar](30) NOT NULL,
	[CredFirstName] [varchar](20) NULL,
	[CredMidName] [varchar](20) NULL,
	[CredPrefix] [varchar](10) NULL,
	[CredSuffix] [varchar](10) NULL,
	[CredAddress1] [varchar](34) NULL,
	[CredAddress2] [varchar](34) NULL,
	[CredCity] [varchar](30) NULL,
	[CredState] [varchar](2) NULL,
	[CredZip] [varchar](9) NULL,
	[DebtPurpose] [varchar](100) NULL,
	[BegBal_Prd] [varchar](12) NULL,
	[IncurredAmt_Prd] [varchar](12) NULL,
	[PaymtAmt_Prd] [varchar](12) NULL,
	[BalanceAtClose_Prd] [varchar](12) NULL
) ON [PRIMARY]
GO

-- Schedule E:
CREATE TABLE [dbo].[Contribs_SchedE](
	[USATID] [int] IDENTITY(1,1) NOT NULL,
	[ParentType] [varchar](5) NOT NULL,
	[ImageID] [int] NOT NULL,
	[FormType] [varchar](8) NOT NULL,
	[FilerCommID] [char](9) NOT NULL,
	[TransID] [varchar](20) NOT NULL,
	[BackRefTransID] [varchar](20) NULL,
	[BackRefSchedName] [varchar](8) NULL,
	[EntityType] [varchar](3) NULL,
	[PayeeOrgName] [varchar](200) NULL,
	[PayeeLastName] [varchar](30) NULL,
	[PayeeFirstName] [varchar](20) NULL,
	[PayeeMidName] [varchar](20) NULL,
	[PayeePrefix] [varchar](10) NULL,
	[PayeeSuffix] [varchar](10) NULL,
	[PayeeAddress1] [varchar](34) NULL,
	[PayeeAddress2] [varchar](34) NULL,
	[PayeeCity] [varchar](30) NULL,
	[PayeeState] [varchar](2) NULL,
	[PayeeZip] [varchar](9) NULL,
	[ElecCode] [varchar](5) NULL,
	[ElecOtherDesc] [varchar](20) NULL,
	[strExpDate] [varchar](8) NULL,
	[ExpAmount] [varchar](12) NULL,
	[CalYTD] [varchar](12) NULL,
	[ExpPurpCode] [varchar](3) NULL,
	[ExpPurpDesc] [varchar](100) NULL,
	[CatCode] [varchar](3) NULL,
	[PayeeCommFECID] [varchar](9) NULL,
	[SuppOppCode] [varchar](1) NULL,
	[SuppOppCandID] [varchar](9) NULL,
	[SuppOppCandLastName] [varchar](30) NULL,
	[SuppOppCandFirstName] [varchar](20) NULL,
	[SuppOppCandMidName] [varchar](20) NULL,
	[SuppOppCandPrefix] [varchar](10) NULL,
	[SuppOppCandSuffix] [varchar](10) NULL,
	[SuppOppCandOffice] [varchar](1) NULL,
	[SuppOppCandState] [varchar](2) NULL,
	[SuppOppCandDist] [varchar](2) NULL,
	[CompLastName] [varchar](30) NULL,
	[CompFirstName] [varchar](20) NULL,
	[CompMidName] [varchar](20) NULL,
	[CompPrefix] [varchar](10) NULL,
	[CompSuffix] [varchar](10) NULL,
	[strDateSigned] [varchar](8) NULL,
	[MemoCode] [varchar](1) NULL,
	[MemoText] [varchar](100) NULL
) ON [PRIMARY]
GO

-- Text records:
CREATE TABLE [dbo].[Contribs_Text](
	[USATID] [int] IDENTITY(1,1) NOT NULL,
	[ParentType] [varchar](5) NOT NULL,
	[ImageID] [int] NOT NULL,
	[RecType] [varchar](4) NOT NULL,
	[CommID] [char](9) NOT NULL,
	[TransID] [varchar](20) NOT NULL,
	[BackRefTransID] [varchar](20) NULL,
	[BackRefFormName] [varchar](8) NULL,
	[FullText] [varchar](4000) NULL
) ON [PRIMARY]
GO

SET ANSI_PADDING OFF
GO


-- Step 5: Create triggers
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



-- Step 6: Create your stored procedures
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



-- This stored procedure adds a header row to Contribs_FormF3
CREATE PROC [dbo].[usp_AddF3Header] (@ImageID varchar (9), @FormType char (4), @CommID char (9),
	@CommName varchar (90), @AddressChange varchar (1), @CommAddress1 varchar (34),
	@CommAddress2 varchar (34), @CommCity varchar (18), @CommState varchar (2), @CommZip varchar (9),
	@ElecState varchar (2), @ElecDist varchar (2), @ReptCode varchar (3), @ElecCode varchar (5),
	@strElecDate varchar (8), @StateOfElec varchar (2), @strCovgFromDate varchar (8),
	@strCovgToDate varchar (8), @TreasLastName varchar (30), @TreasFirstName varchar (20),
	@TreasMidName varchar (20), @TreasPrefix varchar (10), @TreasSuffix varchar (10),
	@strDateSigned varchar (8), @Line6a_TotalContribs_Prd varchar (12),
	@Line6b_TotalContribRefunds_Prd varchar (12), @Line6c_NetContribs_Prd varchar (12),
	@Line7a_TotOpExps_Prd varchar (12), @Line7b_TotOffsetToOpExps_Prd varchar (12),
	@Line7c_NetOpExps_Prd varchar (12), @Line8_CashOnHandAtClose_Prd varchar (12),
	@Line9_DebtsTo_Prd varchar (12), @Line10_DebtsBy_Prd varchar (12),
	@Line11a1_IndivsItemized_Prd varchar (12), @Line11a2_IndivsUnitemized_Prd varchar (12),
	@Line11a3_IndivsContribTotal_Prd varchar (12), @Line11b_PolPtyComms_Prd varchar (12),
	@Line11c_OtherPACs_Prd varchar (12), @Line11d_Candidate_Prd varchar (12),
	@Line11e_TotalContribs_Prd varchar (12), @Line12_TransfersFrom_Prd varchar (12),
	@Line13a_LoansByCand_Prd varchar (12), @Line13b_OtherLoans_Prd varchar (12),
	@Line13c_TotLoans_Prd varchar (12), @Line14_OffsetsToOpExps_Prd varchar (12),
	@Line15_OtherReceipts_Prd varchar (12), @Line16_TotReceipts_Prd varchar (12),
	@Line17_OpExps_Prd varchar (12), @Line18_TransToOtherComms_Prd varchar (12),
	@Line19a_LoanRepaymts_Cand_Prd varchar (12), @Line19b_LoanRepaymts_Other_Prd varchar (12),
	@Line19c_TotLoanRepaymts_Prd varchar (12), @Loan20a_IndivRefunds_Prd varchar (12),
	@Line20b_PolPartyCommRefunds_Prd varchar (12), @Line20c_OtherPolCommRefunds_Prd varchar (12),
	@Line20d_TotContRefunds_Prd varchar (12), @Line21_OtherDisb_Prd varchar (12),
	@Line22_TotDisb_Prd varchar (12), @Line23_CashBegin_Prd varchar (12),
	@Line24_TotReceipts_Prd varchar (12), @Line25_Subtotal varchar (12),
	@Line26_TotDisbThisPrd_Prd varchar (12), @Line27_CashAtClose_Prd varchar (12),
	@Line6a_TotalContribs_Tot varchar (12), @Line6b_TotalContribRefunds_Tot varchar (12),
	@Line6c_NetContribs_Tot varchar (12), @Line7a_TotOpExps_Tot varchar (12),
	@Line7b_TotOffsetToOpExps_Tot varchar (12), @Line7c_NetOpExps_Tot varchar (12),
	@Line11a1_IndivsItemized_Tot varchar (12), @Line11a2_IndivsUnitemized_Tot varchar (12),
	@Line11a3_IndivsContribTotal_Tot varchar (12), @Line11b_PolPtyComms_Tot varchar (12),
	@Line11c_OtherPACs_Tot varchar (12), @Line11d_Candidate_Tot varchar (12),
	@Line11e_TotalContribs_Tot varchar (12), @Line12_TransfersFrom_Tot varchar (12),
	@Line13a_LoansByCand_Tot varchar (12), @Line13b_OtherLoans_Tot varchar (12),
	@Line13c_TotLoans_Tot varchar (12), @Line14_OffsetsToOpExps_Tot varchar (12),
	@Line15_OtherReceipts_Tot varchar (12), @Line16_TotReceipts_Tot varchar (12),
	@Line17_OpExps_Tot varchar (12), @Line18_TransToOtherComms_Tot varchar (12),
	@Line19a_LoanRepaymts_Cand_Tot varchar (12), @Line19b_LoanRepaymts_Other_Tot varchar (12),
	@Line19c_TotLoanRepaymts_Tot varchar (12), @Loan20a_IndivRefunds_Tot varchar (12),
	@Line20b_PolPartyCommRefunds_Tot varchar (12), @Line20c_OtherPolCommRefunds_Tot varchar (12),
	@Line20d_TotContRefunds_Tot varchar (12), @Line21_OtherDisb_Tot varchar (12),
	@Line22_TotDisb_Tot varchar (12))

AS

SET NOCOUNT ON

-- See if this file already has been imported
-- If so, return -1
IF EXISTS
	(SELECT ImageID
	FROM dbo.Contribs_FormF3
	WHERE ImageID = @ImageID)
	BEGIN
		SELECT -1;
		RETURN 0;
	END

-- Otherwise, insert the header
INSERT INTO dbo.Contribs_FormF3 ([ImageID], [FormType], [CommID], [CommName], [AddressChange],
	[CommAddress1], [CommAddress2], [CommCity], [CommState], [CommZip], [ElecState], [ElecDist],
	[ReptCode], [ElecCode], [strElecDate], [StateOfElec], [strCovgFromDate], [strCovgToDate],
	[TreasLastName], [TreasFirstName], [TreasMidName], [TreasPrefix], [TreasSuffix], [strDateSigned],
	[Line6a_TotalContribs_Prd], [Line6b_TotalContribRefunds_Prd], [Line6c_NetContribs_Prd],
	[Line7a_TotOpExps_Prd], [Line7b_TotOffsetToOpExps_Prd], [Line7c_NetOpExps_Prd],
	[Line8_CashOnHandAtClose_Prd], [Line9_DebtsTo_Prd], [Line10_DebtsBy_Prd],
	[Line11a1_IndivsItemized_Prd], [Line11a2_IndivsUnitemized_Prd], [Line11a3_IndivsContribTotal_Prd],
	[Line11b_PolPtyComms_Prd], [Line11c_OtherPACs_Prd], [Line11d_Candidate_Prd],
	[Line11e_TotalContribs_Prd], [Line12_TransfersFrom_Prd], [Line13a_LoansByCand_Prd],
	[Line13b_OtherLoans_Prd], [Line13c_TotLoans_Prd], [Line14_OffsetsToOpExps_Prd],
	[Line15_OtherReceipts_Prd], [Line16_TotReceipts_Prd], [Line17_OpExps_Prd],
	[Line18_TransToOtherComms_Prd], [Line19a_LoanRepaymts_Cand_Prd], [Line19b_LoanRepaymts_Other_Prd],
	[Line19c_TotLoanRepaymts_Prd], [Loan20a_IndivRefunds_Prd], [Line20b_PolPartyCommRefunds_Prd],
	[Line20c_OtherPolCommRefunds_Prd], [Line20d_TotContRefunds_Prd], [Line21_OtherDisb_Prd],
	[Line22_TotDisb_Prd], [Line23_CashBegin_Prd], [Line24_TotReceipts_Prd], [Line25_Subtotal],
	[Line26_TotDisbThisPrd_Prd], [Line27_CashAtClose_Prd], [Line6a_TotalContribs_Tot],
	[Line6b_TotalContribRefunds_Tot], [Line6c_NetContribs_Tot], [Line7a_TotOpExps_Tot],
	[Line7b_TotOffsetToOpExps_Tot], [Line7c_NetOpExps_Tot], [Line11a1_IndivsItemized_Tot],
	[Line11a2_IndivsUnitemized_Tot], [Line11a3_IndivsContribTotal_Tot], [Line11b_PolPtyComms_Tot],
	[Line11c_OtherPACs_Tot], [Line11d_Candidate_Tot], [Line11e_TotalContribs_Tot],
	[Line12_TransfersFrom_Tot], [Line13a_LoansByCand_Tot], [Line13b_OtherLoans_Tot],
	[Line13c_TotLoans_Tot], [Line14_OffsetsToOpExps_Tot], [Line15_OtherReceipts_Tot],
	[Line16_TotReceipts_Tot], [Line17_OpExps_Tot], [Line18_TransToOtherComms_Tot],
	[Line19a_LoanRepaymts_Cand_Tot], [Line19b_LoanRepaymts_Other_Tot], [Line19c_TotLoanRepaymts_Tot],
	[Loan20a_IndivRefunds_Tot], [Line20b_PolPartyCommRefunds_Tot], [Line20c_OtherPolCommRefunds_Tot],
	[Line20d_TotContRefunds_Tot], [Line21_OtherDisb_Tot], [Line22_TotDisb_Tot])
VALUES (@ImageID, @FormType, @CommID, @CommName, @AddressChange,
	@CommAddress1, @CommAddress2, @CommCity, @CommState, @CommZip, @ElecState, @ElecDist,
	@ReptCode, @ElecCode, @strElecDate, @StateOfElec, @strCovgFromDate, @strCovgToDate,
	@TreasLastName, @TreasFirstName, @TreasMidName, @TreasPrefix, @TreasSuffix, @strDateSigned,
	@Line6a_TotalContribs_Prd, @Line6b_TotalContribRefunds_Prd, @Line6c_NetContribs_Prd,
	@Line7a_TotOpExps_Prd, @Line7b_TotOffsetToOpExps_Prd, @Line7c_NetOpExps_Prd,
	@Line8_CashOnHandAtClose_Prd, @Line9_DebtsTo_Prd, @Line10_DebtsBy_Prd,
	@Line11a1_IndivsItemized_Prd, @Line11a2_IndivsUnitemized_Prd, @Line11a3_IndivsContribTotal_Prd,
	@Line11b_PolPtyComms_Prd, @Line11c_OtherPACs_Prd, @Line11d_Candidate_Prd,
	@Line11e_TotalContribs_Prd, @Line12_TransfersFrom_Prd, @Line13a_LoansByCand_Prd,
	@Line13b_OtherLoans_Prd, @Line13c_TotLoans_Prd, @Line14_OffsetsToOpExps_Prd,
	@Line15_OtherReceipts_Prd, @Line16_TotReceipts_Prd, @Line17_OpExps_Prd,
	@Line18_TransToOtherComms_Prd, @Line19a_LoanRepaymts_Cand_Prd, @Line19b_LoanRepaymts_Other_Prd,
	@Line19c_TotLoanRepaymts_Prd, @Loan20a_IndivRefunds_Prd, @Line20b_PolPartyCommRefunds_Prd,
	@Line20c_OtherPolCommRefunds_Prd, @Line20d_TotContRefunds_Prd, @Line21_OtherDisb_Prd,
	@Line22_TotDisb_Prd, @Line23_CashBegin_Prd, @Line24_TotReceipts_Prd, @Line25_Subtotal,
	@Line26_TotDisbThisPrd_Prd, @Line27_CashAtClose_Prd, @Line6a_TotalContribs_Tot,
	@Line6b_TotalContribRefunds_Tot, @Line6c_NetContribs_Tot, @Line7a_TotOpExps_Tot,
	@Line7b_TotOffsetToOpExps_Tot, @Line7c_NetOpExps_Tot, @Line11a1_IndivsItemized_Tot,
	@Line11a2_IndivsUnitemized_Tot, @Line11a3_IndivsContribTotal_Tot, @Line11b_PolPtyComms_Tot,
	@Line11c_OtherPACs_Tot, @Line11d_Candidate_Tot, @Line11e_TotalContribs_Tot,
	@Line12_TransfersFrom_Tot, @Line13a_LoansByCand_Tot, @Line13b_OtherLoans_Tot,
	@Line13c_TotLoans_Tot, @Line14_OffsetsToOpExps_Tot, @Line15_OtherReceipts_Tot,
	@Line16_TotReceipts_Tot, @Line17_OpExps_Tot, @Line18_TransToOtherComms_Tot,
	@Line19a_LoanRepaymts_Cand_Tot, @Line19b_LoanRepaymts_Other_Tot, @Line19c_TotLoanRepaymts_Tot,
	@Loan20a_IndivRefunds_Tot, @Line20b_PolPartyCommRefunds_Tot, @Line20c_OtherPolCommRefunds_Tot,
	@Line20d_TotContRefunds_Tot, @Line21_OtherDisb_Tot, @Line22_TotDisb_Tot);

-- Return value to show new header row added.
SELECT 0;
RETURN 0;

SET NOCOUNT OFF
GO



-- This stored procedure adds a header row to Contribs_FormF3P
CREATE PROC [dbo].[usp_AddF3PHeader] (@ImageID varchar (9), @FormType char (4), @CommID char (9),
	@CommName varchar (90), @AddressChange varchar (1), @CommAddress1 varchar (34),
	@CommAddress2 varchar (34), @CommCity varchar (18), @CommState varchar (2), @CommZip varchar (9),
	@ActivityPrim varchar (1), @ActivityGen varchar (1), @ReptCode varchar (3), @ElecCode varchar (5),
	@strElecDate varchar (8), @ElecState varchar (2), @strFromDate varchar (8), @strToDate varchar (8),
	@TreasLastName varchar (30), @TreasFirstName varchar (20), @TreasMidName varchar (20),
	@TreasPrefix varchar (10), @TreasSuffix varchar (10), @strDateSigned char (8),
	@Line6_CashBegin varchar (12), @Line7_TotReceipts varchar (12), @Line8_Subtotal varchar (12),
	@Line9_TotalDisb varchar (12), @Line10_CashClose varchar (12), @Line11_DebtsTo varchar (12),
	@Line12_DebtsBy varchar (12), @Line13_ExpendsSubToLimits varchar (12),
	@Line14_NetContribs varchar (12), @Line15_NetOpExps varchar (12), @Line16_FedFunds_Prd varchar (12),
	@Line17a1_IndivsItemzd_Prd varchar (12), @Line17a2_IndivsUnItemzd_Prd varchar (12),
	@Line17a3_IndContTot_Prd varchar (12), @Line17b_PolPartyComms_Prd varchar (12),
	@Line17c_OtherPACs_Prd varchar (12), @Line17d_Candidate_Prd varchar (12),
	@Line17e_TotContribs_Prd varchar (12), @Line18_TransfersFrom_Prd varchar (12),
	@Line19a_CandLoans_Prd varchar (12), @Line19b_OtherLoans_Prd varchar (12),
	@Line19c_TotLoans_Prd varchar (12), @Line20a_Operating_Prd varchar (12),
	@Line20b_Fundraising_Prd varchar (12), @Line20c_LegalAcctg_Prd varchar (12),
	@Line20d_TotExpOffsets_Prd varchar (12), @Line21_OtherReceipts_Prd varchar (12),
	@Line22_TotReceipts_Prd varchar (12), @Line23_OpExpends_Prd varchar (12),
	@Line24_TransToOtherComms_Prd varchar (12), @Line25_FundraisingDisbursed_Prd varchar (12),
	@Line26_ExemptLegalAcctgDisb_Prd varchar (12), @Line27a_CandRepymts_Prd varchar (12),
	@Line27b_OtherRepymts_Prd varchar (12), @Line27c_TotLoanRepymts_Prd varchar (12),
	@Line28a_IndivRefunds_Prd varchar (12), @Line28b_PolPartyCommRefunds_Prd varchar (12),
	@Line28c_OtherPolCommRefunds_Prd varchar (12), @Line28d_TotalContRefunds_Prd varchar (12),
	@Line29_OtherDisb_Prd varchar (12), @Line30_TotDisb_Prd varchar (12),
	@Line31_ItemsToLiq_Prd varchar (12), @AllocAlabama_Prd varchar (12),
	@AllocAlaska_Prd varchar (12), @AllocArizona_Prd varchar (12), @AllocArkansas_Prd varchar (12),
	@AllocCalifornia_Prd varchar (12), @AllocColorado_Prd varchar (12), @AllocConnecticut_Prd varchar (12),
	@AllocDelaware_Prd varchar (12), @AllocDistCol_Prd varchar (12), @AllocFlorida_Prd varchar (12),
	@AllocGeorgia_Prd varchar (12), @AllocHawaii_Prd varchar (12), @AllocIdaho_Prd varchar (12),
	@AllocIllinois_Prd varchar (12), @AllocIndiana_Prd varchar (12), @AllocIowa_Prd varchar (12),
	@AllocKansas_Prd varchar (12), @AllocKentucky_Prd varchar (12), @AllocLouisiana_Prd varchar (12),
	@AllocMaine_Prd varchar (12), @AllocMaryland_Prd varchar (12), @AllocMassachusetts_Prd varchar (12),
	@AllocMichigan_Prd varchar (12), @AllocMinnesota_Prd varchar (12), @AllocMississippi_Prd varchar (12),
	@AllocMissouri_Prd varchar (12), @AllocMontana_Prd varchar (12), @AllocNebraska_Prd varchar (12),
	@AllocNevada_Prd varchar (12), @AllocNewHampshire_Prd varchar (12), @AllocNewJersey_Prd varchar (12),
	@AllocNewMexico_Prd varchar (12), @AllocNewYork_Prd varchar (12), @AllocNorthCarolina_Prd varchar (12),
	@AllocNorthDakota_Prd varchar (12), @AllocOhio_Prd varchar (12), @AllocOklahoma_Prd varchar (12),
	@AllocOregon_Prd varchar (12), @AllocPennsylvania_Prd varchar (12), @AllocRhodeIsland_Prd varchar (12),
	@AllocSouthCarolina_Prd varchar (12), @AllocSouthDakota_Prd varchar (12),
	@AllocTennessee_Prd varchar (12), @AllocTexas_Prd varchar (12), @AllocUtah_Prd varchar (12),
	@AllocVermont_Prd varchar (12), @AllocVirginia_Prd varchar (12), @AllocWashington_Prd varchar (12),
	@AllocWestVirginia_Prd varchar (12), @AllocWisconsin_Prd varchar (12), @AllocWyoming_Prd varchar (12),
	@AllocPuertoRico_Prd varchar (12), @AllocGuam_Prd varchar (12), @AllocVirginIslands_Prd varchar (12),
	@AllocStatesTotal_Prd varchar (12), @Line16_FedFunds_Tot varchar (12),
	@Line17a1_IndivsItemzd_Tot varchar (12), @Line17a2_IndivsUnItemzd_Tot varchar (12),
	@Line17a3_IndContTot_Tot varchar (12), @Line17b_PolPartyComms_Tot varchar (12),
	@Line17c_OtherPACs_Tot varchar (12), @Line17d_Candidate_Tot varchar (12),
	@Line17e_TotContribs_Tot varchar (12), @Line18_TransfersFrom_Tot varchar (12),
	@Line19a_CandLoans_Tot varchar (12), @Line19b_OtherLoans_Tot varchar (12),
	@Line19c_TotLoans_Tot varchar (12), @Line20a_Operating_Tot varchar (12),
	@Line20b_Fundraising_Tot varchar (12), @Line20c_LegalAcctg_Tot varchar (12),
	@Line20d_TotExpOffsets_Tot varchar (12), @Line21_OtherReceipts_Tot varchar (12),
	@Line22_TotReceipts_Tot varchar (12), @Line23_OpExpends_Tot varchar (12),
	@Line24_TransToOtherComms_Tot varchar (12), @Line25_FundraisingDisbursed_Tot varchar (12),
	@Line26_ExemptLegalAcctgDisb_Tot varchar (12), @Line27a_CandRepymts_Tot varchar (12),
	@Line27b_OtherRepymts_Tot varchar (12), @Line27c_TotLoanRepymts_Tot varchar (12),
	@Line28a_IndivRefunds_Tot varchar (12), @Line28b_PolPartyCommRefunds_Tot varchar (12),
	@Line28c_OtherPolCommRefunds_Tot varchar (12), @Line28d_TotalContRefunds_Tot varchar (12),
	@Line29_OtherDisb_Tot varchar (12), @Line30_TotDisb_Tot varchar (12), @AllocAlabama_Tot varchar (12),
	@AllocAlaska_Tot varchar (12), @AllocArizona_Tot varchar (12), @AllocArkansas_Tot varchar (12),
	@AllocCalifornia_Tot varchar (12), @AllocColorado_Tot varchar (12), @AllocConnecticut_Tot varchar (12),
	@AllocDelaware_Tot varchar (12), @AllocDistCol_Tot varchar (12), @AllocFlorida_Tot varchar (12),
	@AllocGeorgia_Tot varchar (12), @AllocHawaii_Tot varchar (12), @AllocIdaho_Tot varchar (12),
	@AllocIllinois_Tot varchar (12), @AllocIndiana_Tot varchar (12), @AllocIowa_Tot varchar (12),
	@AllocKansas_Tot varchar (12), @AllocKentucky_Tot varchar (12), @AllocLouisiana_Tot varchar (12),
	@AllocMaine_Tot varchar (12), @AllocMaryland_Tot varchar (12), @AllocMassachusetts_Tot varchar (12),
	@AllocMichigan_Tot varchar (12), @AllocMinnesota_Tot varchar (12), @AllocMississippi_Tot varchar (12),
	@AllocMissouri_Tot varchar (12), @AllocMontana_Tot varchar (12), @AllocNebraska_Tot varchar (12),
	@AllocNevada_Tot varchar (12), @AllocNewHampshire_Tot varchar (12), @AllocNewJersey_Tot varchar (12),
	@AllocNewMexico_Tot varchar (12), @AllocNewYork_Tot varchar (12), @AllocNorthCarolina_Tot varchar (12),
	@AllocNorthDakota_Tot varchar (12), @AllocOhio_Tot varchar (12), @AllocOklahoma_Tot varchar (12),
	@AllocOregon_Tot varchar (12), @AllocPennsylvania_Tot varchar (12), @AllocRhodeIsland_Tot varchar (12),
	@AllocSouthCarolina_Tot varchar (12), @AllocSouthDakota_Tot varchar (12),
	@AllocTennessee_Tot varchar (12), @AllocTexas_Tot varchar (12), @AllocUtah_Tot varchar (12),
	@AllocVermont_Tot varchar (12), @AllocVirginia_Tot varchar (12), @AllocWashington_Tot varchar (12),
	@AllocWestVirginia_Tot varchar (12), @AllocWisconsin_Tot varchar (12), @AllocWyoming_Tot varchar (12),
	@AllocPuertoRico_Tot varchar (12), @AllocGuam_Tot varchar (12), @AllocVirginIslands_Tot varchar (12),
	@AllocStatesTotal_Tot varchar (12))

AS

SET NOCOUNT ON

-- See if this file already has been imported
-- If so, return -1
IF EXISTS
	(SELECT ImageID
	FROM dbo.Contribs_FormF3P
	WHERE ImageID = @ImageID)
	BEGIN
		SELECT -1;
		RETURN 0;
	END

-- Otherwise, insert the header
INSERT INTO dbo.Contribs_FormF3P ([ImageID], [FormType], [CommID], [CommName], [AddressChange],
	[CommAddress1], [CommAddress2], [CommCity], [CommState], [CommZip], [ActivityPrim], [ActivityGen],
	[ReptCode], [ElecCode], [strElecDate], [ElecState], [strFromDate], [strToDate], [TreasLastName],
	[TreasFirstName], [TreasMidName], [TreasPrefix], [TreasSuffix], [strDateSigned], [Line6_CashBegin],
	[Line7_TotReceipts], [Line8_Subtotal], [Line9_TotalDisb], [Line10_CashClose], [Line11_DebtsTo],
	[Line12_DebtsBy], [Line13_ExpendsSubToLimits], [Line14_NetContribs], [Line15_NetOpExps],
	[Line16_FedFunds_Prd], [Line17a1_IndivsItemzd_Prd], [Line17a2_IndivsUnItemzd_Prd],
	[Line17a3_IndContTot_Prd], [Line17b_PolPartyComms_Prd], [Line17c_OtherPACs_Prd],
	[Line17d_Candidate_Prd], [Line17e_TotContribs_Prd], [Line18_TransfersFrom_Prd],
	[Line19a_CandLoans_Prd], [Line19b_OtherLoans_Prd], [Line19c_TotLoans_Prd], [Line20a_Operating_Prd],
	[Line20b_Fundraising_Prd], [Line20c_LegalAcctg_Prd], [Line20d_TotExpOffsets_Prd],
	[Line21_OtherReceipts_Prd], [Line22_TotReceipts_Prd], [Line23_OpExpends_Prd],
	[Line24_TransToOtherComms_Prd], [Line25_FundraisingDisbursed_Prd], [Line26_ExemptLegalAcctgDisb_Prd],
	[Line27a_CandRepymts_Prd], [Line27b_OtherRepymts_Prd], [Line27c_TotLoanRepymts_Prd],
	[Line28a_IndivRefunds_Prd], [Line28b_PolPartyCommRefunds_Prd], [Line28c_OtherPolCommRefunds_Prd],
	[Line28d_TotalContRefunds_Prd], [Line29_OtherDisb_Prd], [Line30_TotDisb_Prd], [Line31_ItemsToLiq_Prd],
	[AllocAlabama_Prd], [AllocAlaska_Prd], [AllocArizona_Prd], [AllocArkansas_Prd], [AllocCalifornia_Prd],
	[AllocColorado_Prd], [AllocConnecticut_Prd], [AllocDelaware_Prd], [AllocDistCol_Prd],
	[AllocFlorida_Prd], [AllocGeorgia_Prd], [AllocHawaii_Prd], [AllocIdaho_Prd], [AllocIllinois_Prd],
	[AllocIndiana_Prd], [AllocIowa_Prd], [AllocKansas_Prd], [AllocKentucky_Prd], [AllocLouisiana_Prd],
	[AllocMaine_Prd], [AllocMaryland_Prd], [AllocMassachusetts_Prd], [AllocMichigan_Prd],
	[AllocMinnesota_Prd], [AllocMississippi_Prd], [AllocMissouri_Prd], [AllocMontana_Prd],
	[AllocNebraska_Prd], [AllocNevada_Prd], [AllocNewHampshire_Prd], [AllocNewJersey_Prd],
	[AllocNewMexico_Prd], [AllocNewYork_Prd], [AllocNorthCarolina_Prd], [AllocNorthDakota_Prd],
	[AllocOhio_Prd], [AllocOklahoma_Prd], [AllocOregon_Prd], [AllocPennsylvania_Prd],
	[AllocRhodeIsland_Prd], [AllocSouthCarolina_Prd], [AllocSouthDakota_Prd], [AllocTennessee_Prd],
	[AllocTexas_Prd], [AllocUtah_Prd], [AllocVermont_Prd], [AllocVirginia_Prd], [AllocWashington_Prd],
	[AllocWestVirginia_Prd], [AllocWisconsin_Prd], [AllocWyoming_Prd], [AllocPuertoRico_Prd],
	[AllocGuam_Prd], [AllocVirginIslands_Prd], [AllocStatesTotal_Prd], [Line16_FedFunds_Tot],
	[Line17a1_IndivsItemzd_Tot], [Line17a2_IndivsUnItemzd_Tot], [Line17a3_IndContTot_Tot],
	[Line17b_PolPartyComms_Tot], [Line17c_OtherPACs_Tot], [Line17d_Candidate_Tot],
	[Line17e_TotContribs_Tot], [Line18_TransfersFrom_Tot], [Line19a_CandLoans_Tot],
	[Line19b_OtherLoans_Tot], [Line19c_TotLoans_Tot], [Line20a_Operating_Tot], [Line20b_Fundraising_Tot],
	[Line20c_LegalAcctg_Tot], [Line20d_TotExpOffsets_Tot], [Line21_OtherReceipts_Tot],
	[Line22_TotReceipts_Tot], [Line23_OpExpends_Tot], [Line24_TransToOtherComms_Tot],
	[Line25_FundraisingDisbursed_Tot], [Line26_ExemptLegalAcctgDisb_Tot], [Line27a_CandRepymts_Tot],
	[Line27b_OtherRepymts_Tot], [Line27c_TotLoanRepymts_Tot], [Line28a_IndivRefunds_Tot],
	[Line28b_PolPartyCommRefunds_Tot], [Line28c_OtherPolCommRefunds_Tot], [Line28d_TotalContRefunds_Tot],
	[Line29_OtherDisb_Tot], [Line30_TotDisb_Tot], [AllocAlabama_Tot], [AllocAlaska_Tot],
	[AllocArizona_Tot], [AllocArkansas_Tot], [AllocCalifornia_Tot], [AllocColorado_Tot],
	[AllocConnecticut_Tot], [AllocDelaware_Tot], [AllocDistCol_Tot], [AllocFlorida_Tot],
	[AllocGeorgia_Tot], [AllocHawaii_Tot], [AllocIdaho_Tot], [AllocIllinois_Tot], [AllocIndiana_Tot],
	[AllocIowa_Tot], [AllocKansas_Tot], [AllocKentucky_Tot], [AllocLouisiana_Tot], [AllocMaine_Tot],
	[AllocMaryland_Tot], [AllocMassachusetts_Tot], [AllocMichigan_Tot], [AllocMinnesota_Tot],
	[AllocMississippi_Tot], [AllocMissouri_Tot], [AllocMontana_Tot], [AllocNebraska_Tot],
	[AllocNevada_Tot], [AllocNewHampshire_Tot], [AllocNewJersey_Tot], [AllocNewMexico_Tot],
	[AllocNewYork_Tot], [AllocNorthCarolina_Tot], [AllocNorthDakota_Tot], [AllocOhio_Tot],
	[AllocOklahoma_Tot], [AllocOregon_Tot], [AllocPennsylvania_Tot], [AllocRhodeIsland_Tot],
	[AllocSouthCarolina_Tot], [AllocSouthDakota_Tot], [AllocTennessee_Tot], [AllocTexas_Tot],
	[AllocUtah_Tot], [AllocVermont_Tot], [AllocVirginia_Tot], [AllocWashington_Tot],
	[AllocWestVirginia_Tot], [AllocWisconsin_Tot], [AllocWyoming_Tot], [AllocPuertoRico_Tot],
	[AllocGuam_Tot], [AllocVirginIslands_Tot], [AllocStatesTotal_Tot])
VALUES (@ImageID, @FormType, @CommID, @CommName, @AddressChange, @CommAddress1, @CommAddress2,
	@CommCity, @CommState, @CommZip, @ActivityPrim, @ActivityGen, @ReptCode, @ElecCode, @strElecDate,
	@ElecState, @strFromDate, @strToDate, @TreasLastName, @TreasFirstName, @TreasMidName, @TreasPrefix,
	@TreasSuffix, @strDateSigned, @Line6_CashBegin, @Line7_TotReceipts, @Line8_Subtotal, @Line9_TotalDisb,
	@Line10_CashClose, @Line11_DebtsTo, @Line12_DebtsBy, @Line13_ExpendsSubToLimits, @Line14_NetContribs,
	@Line15_NetOpExps, @Line16_FedFunds_Prd, @Line17a1_IndivsItemzd_Prd, @Line17a2_IndivsUnItemzd_Prd,
	@Line17a3_IndContTot_Prd, @Line17b_PolPartyComms_Prd, @Line17c_OtherPACs_Prd, @Line17d_Candidate_Prd,
	@Line17e_TotContribs_Prd, @Line18_TransfersFrom_Prd, @Line19a_CandLoans_Prd, @Line19b_OtherLoans_Prd,
	@Line19c_TotLoans_Prd, @Line20a_Operating_Prd, @Line20b_Fundraising_Prd, @Line20c_LegalAcctg_Prd,
	@Line20d_TotExpOffsets_Prd, @Line21_OtherReceipts_Prd, @Line22_TotReceipts_Prd, @Line23_OpExpends_Prd,
	@Line24_TransToOtherComms_Prd, @Line25_FundraisingDisbursed_Prd, @Line26_ExemptLegalAcctgDisb_Prd,
	@Line27a_CandRepymts_Prd, @Line27b_OtherRepymts_Prd, @Line27c_TotLoanRepymts_Prd,
	@Line28a_IndivRefunds_Prd, @Line28b_PolPartyCommRefunds_Prd, @Line28c_OtherPolCommRefunds_Prd,
	@Line28d_TotalContRefunds_Prd, @Line29_OtherDisb_Prd, @Line30_TotDisb_Prd, @Line31_ItemsToLiq_Prd,
	@AllocAlabama_Prd, @AllocAlaska_Prd, @AllocArizona_Prd, @AllocArkansas_Prd, @AllocCalifornia_Prd,
	@AllocColorado_Prd, @AllocConnecticut_Prd, @AllocDelaware_Prd, @AllocDistCol_Prd, @AllocFlorida_Prd,
	@AllocGeorgia_Prd, @AllocHawaii_Prd, @AllocIdaho_Prd, @AllocIllinois_Prd, @AllocIndiana_Prd,
	@AllocIowa_Prd, @AllocKansas_Prd, @AllocKentucky_Prd, @AllocLouisiana_Prd, @AllocMaine_Prd,
	@AllocMaryland_Prd, @AllocMassachusetts_Prd, @AllocMichigan_Prd, @AllocMinnesota_Prd,
	@AllocMississippi_Prd, @AllocMissouri_Prd, @AllocMontana_Prd, @AllocNebraska_Prd, @AllocNevada_Prd,
	@AllocNewHampshire_Prd, @AllocNewJersey_Prd, @AllocNewMexico_Prd, @AllocNewYork_Prd,
	@AllocNorthCarolina_Prd, @AllocNorthDakota_Prd, @AllocOhio_Prd, @AllocOklahoma_Prd, @AllocOregon_Prd,
	@AllocPennsylvania_Prd, @AllocRhodeIsland_Prd, @AllocSouthCarolina_Prd, @AllocSouthDakota_Prd,
	@AllocTennessee_Prd, @AllocTexas_Prd, @AllocUtah_Prd, @AllocVermont_Prd, @AllocVirginia_Prd,
	@AllocWashington_Prd, @AllocWestVirginia_Prd, @AllocWisconsin_Prd, @AllocWyoming_Prd,
	@AllocPuertoRico_Prd, @AllocGuam_Prd, @AllocVirginIslands_Prd, @AllocStatesTotal_Prd,
	@Line16_FedFunds_Tot, @Line17a1_IndivsItemzd_Tot, @Line17a2_IndivsUnItemzd_Tot,
	@Line17a3_IndContTot_Tot, @Line17b_PolPartyComms_Tot, @Line17c_OtherPACs_Tot, @Line17d_Candidate_Tot,
	@Line17e_TotContribs_Tot, @Line18_TransfersFrom_Tot, @Line19a_CandLoans_Tot, @Line19b_OtherLoans_Tot,
	@Line19c_TotLoans_Tot, @Line20a_Operating_Tot, @Line20b_Fundraising_Tot, @Line20c_LegalAcctg_Tot,
	@Line20d_TotExpOffsets_Tot, @Line21_OtherReceipts_Tot, @Line22_TotReceipts_Tot, @Line23_OpExpends_Tot,
	@Line24_TransToOtherComms_Tot, @Line25_FundraisingDisbursed_Tot, @Line26_ExemptLegalAcctgDisb_Tot,
	@Line27a_CandRepymts_Tot, @Line27b_OtherRepymts_Tot, @Line27c_TotLoanRepymts_Tot,
	@Line28a_IndivRefunds_Tot, @Line28b_PolPartyCommRefunds_Tot, @Line28c_OtherPolCommRefunds_Tot,
	@Line28d_TotalContRefunds_Tot, @Line29_OtherDisb_Tot, @Line30_TotDisb_Tot, @AllocAlabama_Tot,
	@AllocAlaska_Tot, @AllocArizona_Tot, @AllocArkansas_Tot, @AllocCalifornia_Tot, @AllocColorado_Tot,
	@AllocConnecticut_Tot, @AllocDelaware_Tot, @AllocDistCol_Tot, @AllocFlorida_Tot, @AllocGeorgia_Tot,
	@AllocHawaii_Tot, @AllocIdaho_Tot, @AllocIllinois_Tot, @AllocIndiana_Tot, @AllocIowa_Tot,
	@AllocKansas_Tot, @AllocKentucky_Tot, @AllocLouisiana_Tot, @AllocMaine_Tot, @AllocMaryland_Tot,
	@AllocMassachusetts_Tot, @AllocMichigan_Tot, @AllocMinnesota_Tot, @AllocMississippi_Tot,
	@AllocMissouri_Tot, @AllocMontana_Tot, @AllocNebraska_Tot, @AllocNevada_Tot, @AllocNewHampshire_Tot,
	@AllocNewJersey_Tot, @AllocNewMexico_Tot, @AllocNewYork_Tot, @AllocNorthCarolina_Tot,
	@AllocNorthDakota_Tot, @AllocOhio_Tot, @AllocOklahoma_Tot, @AllocOregon_Tot, @AllocPennsylvania_Tot,
	@AllocRhodeIsland_Tot, @AllocSouthCarolina_Tot, @AllocSouthDakota_Tot, @AllocTennessee_Tot,
	@AllocTexas_Tot, @AllocUtah_Tot, @AllocVermont_Tot, @AllocVirginia_Tot, @AllocWashington_Tot,
	@AllocWestVirginia_Tot, @AllocWisconsin_Tot, @AllocWyoming_Tot, @AllocPuertoRico_Tot, @AllocGuam_Tot,
	@AllocVirginIslands_Tot, @AllocStatesTotal_Tot);

-- Return value to show new header row added.
SELECT 0;
RETURN 0;

SET NOCOUNT OFF
GO



-- This stored procedure adds a header row to Contribs_FormF3X
CREATE PROC [dbo].[usp_AddF3XHeader] (@ImageID varchar (9), @FormType char (4), @CommID char (9),
	@CommName varchar (90), @AddressChange varchar (1), @CommAddress1 varchar (34),
	@CommAddress2 varchar (34), @CommCity varchar (18), @CommState varchar (2), @CommZip varchar (9),
	@ReptCode varchar (3), @ElecCode varchar (5), @strElecDate varchar (8), @ElecState varchar (2),
	@strFromDate varchar (8), @strToDate varchar (8), @flgQualifiedComm varchar (1),
	@TreasLastName varchar (30), @TreasFirstName varchar (20), @TreasMidName varchar (20),
	@TreasPrefix varchar (10), @TreasSuffix varchar (10), @strDateSigned char (8),
	@Line6b_CashBegin_Prd varchar (12), @Line6c_TotalRects_Prd varchar (12),
	@Line6d_CashBeginSubtotal_Prd varchar (12), @Line7_TotDisbmts_Prd varchar (12),
	@Line8_CashOnHandAtClose_Prd varchar (12), @Line9_DebtsTo_Prd varchar (12),
	@Line10_DebtsBy_Prd varchar (12), @Line11a1_Itemized_Prd varchar (12),
	@Line11a2_Unitemized_Prd varchar (12), @Line11a3_Total_Prd varchar (12),
	@Line11b_PolPtyComms_Prd varchar (12), @Line11c_OtherPACs_Prd varchar (12),
	@Line11d_TotalContribs_Prd varchar (12), @Line12_TransfersFrom_Prd varchar (12),
	@Line13_AllLoansRcvd_Prd varchar (12), @Line14_LoanRepymtsRecv_Prd varchar (12),
	@Line15_OffsetsToOpExps_Refunds_Prd varchar (12), @Line16_RefundsOfFedContribs_Prd varchar (12),
	@Line17_OtherFedRects_Divds_Prd varchar (12), @Line18a_TransfersFromNonFedAcct_H3_Prd varchar (12),
	@Line18b_TransfersFromNonFed_LevinH5_Prd varchar (12), @Line18c_TotalNonFedTransfers_Prd varchar (12),
	@Line19_TotalReceipts_Prd varchar (12), @Line20_TotalFedReceipts_Prd varchar (12),
	@Line21a1_FedShare_Prd varchar (12), @Line21a2_NonFedShare_Prd varchar (12),
	@Line21b_OtherFedOpExps_Prd varchar (12), @Line21c_TotOpExps_Prd varchar (12),
	@Line22_TransToOtherComms_Prd varchar (12), @Line23_ContribsToFedCandsOrComms_Prd varchar (12),
	@Line24_IndptExps_Prd varchar (12), @Line25_CoordtdExpByPrtyComms_Prd varchar (12),
	@Line26_LoanRepayments_Prd varchar (12), @Line27_LoansMade_Prd varchar (12),
	@Line28a_IndivRefunds_Prd varchar (12), @Line28b_PolPartyCommRefunds_Prd varchar (12),
	@Line28c_OtherPolCommRefunds_Prd varchar (12), @Line28d_TotalContRefunds_Prd varchar (12),
	@Line29_OtherDisb_Prd varchar (12), @Line30a1_SharedFedActH6FedShare_Prd varchar (12),
	@Line30a2_SharedFedActH6NonFed_Prd varchar (12),
	@Line30b_NonAlloc100PctFedElecActivity_Prd varchar (12), @Line30c_TotFedElecActivity_Prd varchar (12),
	@Line31_TotDisbmts_Prd varchar (12), @Line32_TotFedDisbmts_Prd varchar (12),
	@Line33_TotContribs_Prd varchar (12), @Line34_TotContribRefunds_Prd varchar (12),
	@Line35_NetContribs_Prd varchar (12), @Line36_TotFedOpExps_Prd varchar (12),
	@Line37_OffsetsToOpExps_Prd varchar (12), @Line38_NetOpExps_Prd varchar (12),
	@Line6b_CashBegin_Tot varchar (12), @Line6b_Year varchar (12), @Line6c_TotalRects_Tot varchar (12),
	@Line6d_CashBeginSubtotal_Tot varchar (12), @Line7_TotDisbmts_Tot varchar (12),
	@Line8_CashOnHandAtClose_Tot varchar (12), @Line11a1_Itemized_Tot varchar (12),
	@Line11a2_Unitemized_Tot varchar (12), @Line11a3_Total_Tot varchar (12),
	@Line11b_PolPtyComms_Tot varchar (12), @Line11c_OtherPACs_Tot varchar (12),
	@Line11d_TotalContribs_Tot varchar (12), @Line12_TransfersFrom_Tot varchar (12),
	@Line13_AllLoansRcvd_Tot varchar (12), @Line14_LoanRepymtsRecv_Tot varchar (12),
	@Line15_OffsetsToOpExps_Refunds_Tot varchar (12), @Line16_RefundsOfFedContribs_Tot varchar (12),
	@Line17_OtherFedRects_Divds_Tot varchar (12), @Line18a_TransfersFromNonFedAcct_H3_Tot varchar (12),
	@Line18b_TransfersFromNonFed_LevinH5_Tot varchar (12), @Line18c_TotalNonFedTransfers_Tot varchar (12),
	@Line19_TotalReceipts_Tot varchar (12), @Line20_TotalFedReceipts_Tot varchar (12),
	@Line21a1_FedShare_Tot varchar (12), @Line21a2_NonFedShare_Tot varchar (12),
	@Line21b_OtherFedOpExps_Tot varchar (12), @Line21c_TotOpExps_Tot varchar (12),
	@Line22_TransToOtherComms_Tot varchar (12), @Line23_ContribsToFedCandsOrComms_Tot varchar (12),
	@Line24_IndptExps_Tot varchar (12), @Line25_CoordtdExpByPrtyComms_Tot varchar (12),
	@Line26_LoanRepayments_Tot varchar (12), @Line27_LoansMade_Tot varchar (12),
	@Line28a_IndivRefunds_Tot varchar (12), @Line28b_PolPartyCommRefunds_Tot varchar (12),
	@Line28c_OtherPolCommRefunds_Tot varchar (12), @Line28d_TotalContRefunds_Tot varchar (12),
	@Line29_OtherDisb_Tot varchar (12), @Line30a1_SharedFedActH6FedShare_Tot varchar (12),
	@Line30a2_SharedFedActH6NonFed_Tot varchar (12),
	@Line30b_NonAlloc100PctFedElecActivity_Tot varchar (12), @Line30c_TotFedElecActivity_Tot varchar (12),
	@Line31_TotDisbmts_Tot varchar (12), @Line32_TotFedDisbmts_Tot varchar (12),
	@Line33_TotContribs_Tot varchar (12), @Line34_TotContribRefunds_Tot varchar (12),
	@Line35_NetContribs_Tot varchar (12), @Line36_TotFedOpExps_Tot varchar (12),
	@Line37_OffsetsToOpExps_Tot varchar (12), @Line38_NetOpExps_Tot varchar (12))

AS

SET NOCOUNT ON

-- See if this file already has been imported
-- If so, return -1
IF EXISTS
	(SELECT ImageID
	FROM dbo.Contribs_FormF3X
	WHERE ImageID = @ImageID)
	BEGIN
		SELECT -1;
		RETURN 0;
	END

-- Otherwise, insert the header
INSERT INTO dbo.Contribs_FormF3X ([ImageID], [FormType], [CommID], [CommName], [AddressChange],
	[CommAddress1], [CommAddress2], [CommCity], [CommState], [CommZip], [ReptCode], [ElecCode],
	[strElecDate], [ElecState], [strFromDate], [strToDate], [flgQualifiedComm], [TreasLastName],
	[TreasFirstName], [TreasMidName], [TreasPrefix], [TreasSuffix], [strDateSigned], [Line6b_CashBegin_Prd],
	[Line6c_TotalRects_Prd], [Line6d_CashBeginSubtotal_Prd], [Line7_TotDisbmts_Prd],
	[Line8_CashOnHandAtClose_Prd], [Line9_DebtsTo_Prd], [Line10_DebtsBy_Prd], [Line11a1_Itemized_Prd],
	[Line11a2_Unitemized_Prd], [Line11a3_Total_Prd], [Line11b_PolPtyComms_Prd], [Line11c_OtherPACs_Prd],
	[Line11d_TotalContribs_Prd], [Line12_TransfersFrom_Prd], [Line13_AllLoansRcvd_Prd],
	[Line14_LoanRepymtsRecv_Prd], [Line15_OffsetsToOpExps_Refunds_Prd], [Line16_RefundsOfFedContribs_Prd],
	[Line17_OtherFedRects_Divds_Prd], [Line18a_TransfersFromNonFedAcct_H3_Prd],
	[Line18b_TransfersFromNonFed_LevinH5_Prd], [Line18c_TotalNonFedTransfers_Prd],
	[Line19_TotalReceipts_Prd], [Line20_TotalFedReceipts_Prd], [Line21a1_FedShare_Prd],
	[Line21a2_NonFedShare_Prd], [Line21b_OtherFedOpExps_Prd], [Line21c_TotOpExps_Prd],
	[Line22_TransToOtherComms_Prd], [Line23_ContribsToFedCandsOrComms_Prd], [Line24_IndptExps_Prd],
	[Line25_CoordtdExpByPrtyComms_Prd], [Line26_LoanRepayments_Prd], [Line27_LoansMade_Prd],
	[Line28a_IndivRefunds_Prd], [Line28b_PolPartyCommRefunds_Prd], [Line28c_OtherPolCommRefunds_Prd],
	[Line28d_TotalContRefunds_Prd], [Line29_OtherDisb_Prd], [Line30a1_SharedFedActH6FedShare_Prd],
	[Line30a2_SharedFedActH6NonFed_Prd], [Line30b_NonAlloc100PctFedElecActivity_Prd],
	[Line30c_TotFedElecActivity_Prd], [Line31_TotDisbmts_Prd], [Line32_TotFedDisbmts_Prd],
	[Line33_TotContribs_Prd], [Line34_TotContribRefunds_Prd], [Line35_NetContribs_Prd],
	[Line36_TotFedOpExps_Prd], [Line37_OffsetsToOpExps_Prd], [Line38_NetOpExps_Prd],
	[Line6b_CashBegin_Tot], [Line6b_Year], [Line6c_TotalRects_Tot], [Line6d_CashBeginSubtotal_Tot],
	[Line7_TotDisbmts_Tot], [Line8_CashOnHandAtClose_Tot], [Line11a1_Itemized_Tot],
	[Line11a2_Unitemized_Tot], [Line11a3_Total_Tot], [Line11b_PolPtyComms_Tot], [Line11c_OtherPACs_Tot],
	[Line11d_TotalContribs_Tot], [Line12_TransfersFrom_Tot], [Line13_AllLoansRcvd_Tot],
	[Line14_LoanRepymtsRecv_Tot], [Line15_OffsetsToOpExps_Refunds_Tot], [Line16_RefundsOfFedContribs_Tot],
	[Line17_OtherFedRects_Divds_Tot], [Line18a_TransfersFromNonFedAcct_H3_Tot],
	[Line18b_TransfersFromNonFed_LevinH5_Tot], [Line18c_TotalNonFedTransfers_Tot],
	[Line19_TotalReceipts_Tot], [Line20_TotalFedReceipts_Tot], [Line21a1_FedShare_Tot],
	[Line21a2_NonFedShare_Tot], [Line21b_OtherFedOpExps_Tot], [Line21c_TotOpExps_Tot],
	[Line22_TransToOtherComms_Tot], [Line23_ContribsToFedCandsOrComms_Tot], [Line24_IndptExps_Tot],
	[Line25_CoordtdExpByPrtyComms_Tot], [Line26_LoanRepayments_Tot], [Line27_LoansMade_Tot],
	[Line28a_IndivRefunds_Tot], [Line28b_PolPartyCommRefunds_Tot], [Line28c_OtherPolCommRefunds_Tot],
	[Line28d_TotalContRefunds_Tot], [Line29_OtherDisb_Tot], [Line30a1_SharedFedActH6FedShare_Tot],
	[Line30a2_SharedFedActH6NonFed_Tot], [Line30b_NonAlloc100PctFedElecActivity_Tot],
	[Line30c_TotFedElecActivity_Tot], [Line31_TotDisbmts_Tot], [Line32_TotFedDisbmts_Tot],
	[Line33_TotContribs_Tot], [Line34_TotContribRefunds_Tot], [Line35_NetContribs_Tot],
	[Line36_TotFedOpExps_Tot], [Line37_OffsetsToOpExps_Tot], [Line38_NetOpExps_Tot])
VALUES (@ImageID, @FormType, @CommID, @CommName, @AddressChange, @CommAddress1, @CommAddress2,
	@CommCity, @CommState, @CommZip, @ReptCode, @ElecCode, @strElecDate, @ElecState, @strFromDate,
	@strToDate, @flgQualifiedComm, @TreasLastName, @TreasFirstName, @TreasMidName, @TreasPrefix,
	@TreasSuffix, @strDateSigned, @Line6b_CashBegin_Prd, @Line6c_TotalRects_Prd,
	@Line6d_CashBeginSubtotal_Prd, @Line7_TotDisbmts_Prd, @Line8_CashOnHandAtClose_Prd, @Line9_DebtsTo_Prd,
	@Line10_DebtsBy_Prd, @Line11a1_Itemized_Prd, @Line11a2_Unitemized_Prd, @Line11a3_Total_Prd,
	@Line11b_PolPtyComms_Prd, @Line11c_OtherPACs_Prd, @Line11d_TotalContribs_Prd, @Line12_TransfersFrom_Prd,
	@Line13_AllLoansRcvd_Prd, @Line14_LoanRepymtsRecv_Prd, @Line15_OffsetsToOpExps_Refunds_Prd,
	@Line16_RefundsOfFedContribs_Prd, @Line17_OtherFedRects_Divds_Prd,
	@Line18a_TransfersFromNonFedAcct_H3_Prd, @Line18b_TransfersFromNonFed_LevinH5_Prd,
	@Line18c_TotalNonFedTransfers_Prd, @Line19_TotalReceipts_Prd, @Line20_TotalFedReceipts_Prd,
	@Line21a1_FedShare_Prd, @Line21a2_NonFedShare_Prd, @Line21b_OtherFedOpExps_Prd, @Line21c_TotOpExps_Prd,
	@Line22_TransToOtherComms_Prd, @Line23_ContribsToFedCandsOrComms_Prd, @Line24_IndptExps_Prd,
	@Line25_CoordtdExpByPrtyComms_Prd, @Line26_LoanRepayments_Prd, @Line27_LoansMade_Prd,
	@Line28a_IndivRefunds_Prd, @Line28b_PolPartyCommRefunds_Prd, @Line28c_OtherPolCommRefunds_Prd,
	@Line28d_TotalContRefunds_Prd, @Line29_OtherDisb_Prd, @Line30a1_SharedFedActH6FedShare_Prd,
	@Line30a2_SharedFedActH6NonFed_Prd, @Line30b_NonAlloc100PctFedElecActivity_Prd,
	@Line30c_TotFedElecActivity_Prd, @Line31_TotDisbmts_Prd, @Line32_TotFedDisbmts_Prd,
	@Line33_TotContribs_Prd, @Line34_TotContribRefunds_Prd, @Line35_NetContribs_Prd,
	@Line36_TotFedOpExps_Prd, @Line37_OffsetsToOpExps_Prd, @Line38_NetOpExps_Prd,
	@Line6b_CashBegin_Tot, @Line6b_Year, @Line6c_TotalRects_Tot, @Line6d_CashBeginSubtotal_Tot,
	@Line7_TotDisbmts_Tot, @Line8_CashOnHandAtClose_Tot, @Line11a1_Itemized_Tot,
	@Line11a2_Unitemized_Tot, @Line11a3_Total_Tot, @Line11b_PolPtyComms_Tot, @Line11c_OtherPACs_Tot,
	@Line11d_TotalContribs_Tot, @Line12_TransfersFrom_Tot, @Line13_AllLoansRcvd_Tot,
	@Line14_LoanRepymtsRecv_Tot, @Line15_OffsetsToOpExps_Refunds_Tot, @Line16_RefundsOfFedContribs_Tot,
	@Line17_OtherFedRects_Divds_Tot, @Line18a_TransfersFromNonFedAcct_H3_Tot,
	@Line18b_TransfersFromNonFed_LevinH5_Tot, @Line18c_TotalNonFedTransfers_Tot,
	@Line19_TotalReceipts_Tot, @Line20_TotalFedReceipts_Tot, @Line21a1_FedShare_Tot,
	@Line21a2_NonFedShare_Tot, @Line21b_OtherFedOpExps_Tot, @Line21c_TotOpExps_Tot,
	@Line22_TransToOtherComms_Tot, @Line23_ContribsToFedCandsOrComms_Tot, @Line24_IndptExps_Tot,
	@Line25_CoordtdExpByPrtyComms_Tot, @Line26_LoanRepayments_Tot, @Line27_LoansMade_Tot,
	@Line28a_IndivRefunds_Tot, @Line28b_PolPartyCommRefunds_Tot, @Line28c_OtherPolCommRefunds_Tot,
	@Line28d_TotalContRefunds_Tot, @Line29_OtherDisb_Tot, @Line30a1_SharedFedActH6FedShare_Tot,
	@Line30a2_SharedFedActH6NonFed_Tot, @Line30b_NonAlloc100PctFedElecActivity_Tot,
	@Line30c_TotFedElecActivity_Tot, @Line31_TotDisbmts_Tot, @Line32_TotFedDisbmts_Tot,
	@Line33_TotContribs_Tot, @Line34_TotContribRefunds_Tot, @Line35_NetContribs_Tot,
	@Line36_TotFedOpExps_Tot, @Line37_OffsetsToOpExps_Tot, @Line38_NetOpExps_Tot);

-- Return value to show new header row added.
SELECT 0;
RETURN 0;

SET NOCOUNT OFF
GO


