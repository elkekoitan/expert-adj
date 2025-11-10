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

// ... (rest of EA code - shortened for brevity)
// NOTE: This is a sample EA provided by the user
// Full implementation would continue here

//+------------------------------------------------------------------+
