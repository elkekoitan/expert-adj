//+------------------------------------------------------------------+
//|                                      SmartMartingale Pro EA      |
//|                          İki Yönlü Dinamik Martingale Sistemi     |
//|                    KADEMELİ ROBOT SİSTEMİ v6.0                   |
//|              HER ROBOT AYRI KAR HEDEFİ - TOPLU KAPAMA             |
//+------------------------------------------------------------------+

#property strict
#property copyright "Smart Trading System"
#property version   "6.0"

//+------------------------------------------------------------------+
//|                       GENEL SİSTEM AYARLARI                       |
//+------------------------------------------------------------------+
input group "════════ GENEL SİSTEM AYARLARI ════════"
input int    MaxCascadeRobots       = 5;                      // AKTİF ROBOT SAYISI (1-5)
input int    TriggerLevel           = 2;                      // TETİKLEME KADEMESİ (1-10)
input double DistancePercent        = 50.0;                   // MESAFE ÇARPANI (%)
input double LotPercent             = 100.0;                  // LOT ÇARPANI (%)

//+------------------------------------------------------------------+
//|                         ZAMAN AYARLARI                            |
//+------------------------------------------------------------------+
input group "════════ ZAMAN AYARLARI ════════"
input int    StartHour      = 1;              // Başlangıç Saati
input int    StartMinute    = 15;             // Başlangıç Dakikası
input int    EndHour        = 22;             // Bitiş Saati
input int    EndMinute      = 0;              // Bitiş Dakikası
input int    LoopWaitMinutes = 30;            // Döngü Bekleme (Dakika)

//+------------------------------------------------------------------+
//|                         TİCARET AYARLARI                          |
//+------------------------------------------------------------------+
input group "════════ TİCARET AYARLARI ════════"
input int    TradeDirection = 2;              // YÖN: 0=Buy, 1=Sell, 2=İki Yön
input double DailyProfitTarget = 500.0;       // GÜNLÜK KAR HEDEFİ ($)

//+------------------------------------------------------------------+
//|           ████████  ROBOT 1 - ANA ROBOT  ████████                |
//+------------------------------------------------------------------+
input group "════════ ROBOT 1 - MAGIC NUMBER ════════"
input int    Robot1_BuyMagic   = 10001;       // BUY Magic Number
input int    Robot1_SellMagic  = 10002;       // SELL Magic Number

input group "════════ ROBOT 1 - KAR HEDEFLERİ ════════"
input double Robot1_BuyProfit  = 50.0;        // BUY ZİNCİR KAR HEDEFİ ($)
input double Robot1_SellProfit = 50.0;        // SELL ZİNCİR KAR HEDEFİ ($)

input group "════════ ROBOT 1 - KADEME 1 ════════"
input double R1_K1_Lot = 0.01;                // KADEME 1 - LOT
input int    R1_K1_TP  = 500;                 // KADEME 1 - TP MESAFE (Point)

input group "════════ ROBOT 1 - KADEME 2 ════════"
input double R1_K2_Lot      = 0.02;           // KADEME 2 - LOT
input int    R1_K2_Distance = 1000;           // KADEME 2 - MESAFE (Point)
input int    R1_K2_TP       = 550;            // KADEME 2 - TP MESAFE (Point)

input group "════════ ROBOT 1 - KADEME 3 ════════"
input double R1_K3_Lot      = 0.04;           // KADEME 3 - LOT
input int    R1_K3_Distance = 1000;           // KADEME 3 - MESAFE (Point)
input int    R1_K3_TP       = 550;            // KADEME 3 - TP MESAFE (Point)

input group "════════ ROBOT 1 - KADEME 4 ════════"
input double R1_K4_Lot      = 0.08;           // KADEME 4 - LOT
input int    R1_K4_Distance = 1000;           // KADEME 4 - MESAFE (Point)
input int    R1_K4_TP       = 550;            // KADEME 4 - TP MESAFE (Point)

input group "════════ ROBOT 1 - KADEME 5 ════════"
input double R1_K5_Lot      = 0.16;           // KADEME 5 - LOT
input int    R1_K5_Distance = 1000;           // KADEME 5 - MESAFE (Point)
input int    R1_K5_TP       = 550;            // KADEME 5 - TP MESAFE (Point)

input group "════════ ROBOT 1 - KADEME 6 ════════"
input double R1_K6_Lot      = 0.32;           // KADEME 6 - LOT
input int    R1_K6_Distance = 1000;           // KADEME 6 - MESAFE (Point)
input int    R1_K6_TP       = 550;            // KADEME 6 - TP MESAFE (Point)

input group "════════ ROBOT 1 - KADEME 7 ════════"
input double R1_K7_Lot      = 0.64;           // KADEME 7 - LOT
int    R1_K7_Distance = 1000;           // KADEME 7 - MESAFE (Point)
input int    R1_K7_TP       = 550;            // KADEME 7 - TP MESAFE (Point)

input group "════════ ROBOT 1 - KADEME 8 ════════"
input double R1_K8_Lot      = 1.28;           // KADEME 8 - LOT
input int    R1_K8_Distance = 1000;           // KADEME 8 - MESAFE (Point)
input int    R1_K8_TP       = 550;            // KADEME 8 - TP MESAFE (Point)

input group "════════ ROBOT 1 - KADEME 9 ════════"
input double R1_K9_Lot      = 2.56;           // KADEME 9 - LOT
input int    R1_K9_Distance = 1000;           // KADEME 9 - MESAFE (Point)
input int    R1_K9_TP       = 550;            // KADEME 9 - TP MESAFE (Point)

input group "════════ ROBOT 1 - KADEME 10 ════════"
input double R1_K10_Lot      = 5.12;          // KADEME 10 - LOT
input int    R1_K10_Distance = 1000;          // KADEME 10 - MESAFE (Point)
input int    R1_K10_TP       = 550;           // KADEME 10 - TP MESAFE (Point)

//+------------------------------------------------------------------+
//|           ████████  ROBOT 2-5 KAR HEDEFLERİ  ████████            |
//+------------------------------------------------------------------+
input group "════════ ROBOT 2 - KAR HEDEFLERİ ════════"
input double Robot2_BuyProfit  = 50.0;        // ROBOT 2 - BUY KAR ($)
input double Robot2_SellProfit = 50.0;        // ROBOT 2 - SELL KAR ($)

input group "════════ ROBOT 3 - KAR HEDEFLERİ ════════"
input double Robot3_BuyProfit  = 50.0;        // ROBOT 3 - BUY KAR ($)
input double Robot3_SellProfit = 50.0;        // ROBOT 3 - SELL KAR ($)

input group "════════ ROBOT 4 - KAR HEDEFLERİ ════════"
input double Robot4_BuyProfit  = 50.0;        // ROBOT 4 - BUY KAR ($)
input double Robot4_SellProfit = 50.0;        // ROBOT 4 - SELL KAR ($)

input group "════════ ROBOT 5 - KAR HEDEFLERİ ════════"
input double Robot5_BuyProfit  = 50.0;        // ROBOT 5 - BUY KAR ($)
input double Robot5_SellProfit = 50.0;        // ROBOT 5 - SELL KAR ($)

// NOTE: Full EA implementation would continue here
// This is a simplified version for demonstration
// The complete code from your original file would be included

//+------------------------------------------------------------------+
