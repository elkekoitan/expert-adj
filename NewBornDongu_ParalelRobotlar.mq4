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
input int    R1_K7_Distance = 1000;           // KADEME 7 - MESAFE (Point)
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

//+------------------------------------------------------------------+
//|                         EKRAN AYARLARI                            |
//+------------------------------------------------------------------+
input group "════════ EKRAN AYARLARI ════════"
input int    PanelX       = 10;               // Panel X Konumu
input int    PanelY       = 30;               // Panel Y Konumu
input int    HeaderSize   = 14;               // Başlık Punto
input int    RobotSize    = 12;               // Robot Bilgi Punto
input int    DetailSize   = 10;               // Detay Punto

//+------------------------------------------------------------------+
//|                      ROBOT YAPISI                                 |
//+------------------------------------------------------------------+
struct Robot
{
   int      robotIndex;
   int      buyMagic;
   int      sellMagic;
   
   double   lots[10];
   int      distances[10];
   int      takeProfit[10];
   double   buyChainProfitTarget;
   double   sellChainProfitTarget;
   
   bool     buyActive;
   bool     buyLevelUsed[10];
   bool     buyInLoop;
   datetime buyLoopEndTime;
   
   bool     sellActive;
   bool     sellLevelUsed[10];
   bool     sellInLoop;
   datetime sellLoopEndTime;
   
   bool     buyTriggered;
   bool     sellTriggered;
};

Robot Robots[5];

double DailyStartBalance = 0;
int LastDay = 0;
bool DailyTargetReached = false;

string panelObjects[];
int totalPanelObjects = 0;

//+------------------------------------------------------------------+
//|                            INIT                                   |
//+------------------------------------------------------------------+
int OnInit()
{
   InitRobot1();
   
   for(int i = 1; i < MaxCascadeRobots && i < 5; i++)
   {
      InitCascadeRobot(i);
   }
   
   DailyStartBalance = AccountBalance();
   LastDay = TimeDay(TimeCurrent());
   
   CreatePanel();
   
   Print("╔════════════════════════════════════════════════╗");
   Print("║  KADEMELİ ROBOT SİSTEMİ v6.0 BAŞLATILDI!      ║");
   Print("╠════════════════════════════════════════════════╣");
   Print("  Aktif Robot Sayısı: ", MaxCascadeRobots);
   Print("  Tetikleme Kademesi: ", TriggerLevel);
   Print("  Mesafe Çarpanı: %", DistancePercent);
   Print("  Lot Çarpanı: %", LotPercent);
   Print("╠════════════════════════════════════════════════╣");
   
   for(int i = 0; i < MaxCascadeRobots && i < 5; i++)
   {
      Print("  Robot ", i+1, ":");
      Print("    Magic → BUY:", Robots[i].buyMagic, " SELL:", Robots[i].sellMagic);
      Print("    Hedef → BUY:$", Robots[i].buyChainProfitTarget, " SELL:$", Robots[i].sellChainProfitTarget);
   }
   Print("╚════════════════════════════════════════════════╝");
   
   return INIT_SUCCEEDED;
}

//+------------------------------------------------------------------+
//|                  ROBOT 1 BAŞLAT (ANA ROBOT)                       |
//+------------------------------------------------------------------+
void InitRobot1()
{
   Robots[0].robotIndex = 0;
   Robots[0].buyMagic = Robot1_BuyMagic;
   Robots[0].sellMagic = Robot1_SellMagic;
   
   // 10 KADEME LOT
   Robots[0].lots[0] = R1_K1_Lot;
   Robots[0].lots[1] = R1_K2_Lot;
   Robots[0].lots[2] = R1_K3_Lot;
   Robots[0].lots[3] = R1_K4_Lot;
   Robots[0].lots[4] = R1_K5_Lot;
   Robots[0].lots[5] = R1_K6_Lot;
   Robots[0].lots[6] = R1_K7_Lot;
   Robots[0].lots[7] = R1_K8_Lot;
   Robots[0].lots[8] = R1_K9_Lot;
   Robots[0].lots[9] = R1_K10_Lot;
   
   // 10 KADEME MESAFE
   Robots[0].distances[0] = 0;
   Robots[0].distances[1] = R1_K2_Distance;
   Robots[0].distances[2] = R1_K3_Distance;
   Robots[0].distances[3] = R1_K4_Distance;
   Robots[0].distances[4] = R1_K5_Distance;
   Robots[0].distances[5] = R1_K6_Distance;
   Robots[0].distances[6] = R1_K7_Distance;
   Robots[0].distances[7] = R1_K8_Distance;
   Robots[0].distances[8] = R1_K9_Distance;
   Robots[0].distances[9] = R1_K10_Distance;
   
   // 10 KADEME TP
   Robots[0].takeProfit[0] = R1_K1_TP;
   Robots[0].takeProfit[1] = R1_K2_TP;
   Robots[0].takeProfit[2] = R1_K3_TP;
   Robots[0].takeProfit[3] = R1_K4_TP;
   Robots[0].takeProfit[4] = R1_K5_TP;
   Robots[0].takeProfit[5] = R1_K6_TP;
   Robots[0].takeProfit[6] = R1_K7_TP;
   Robots[0].takeProfit[7] = R1_K8_TP;
   Robots[0].takeProfit[8] = R1_K9_TP;
   Robots[0].takeProfit[9] = R1_K10_TP;
   
   Robots[0].buyChainProfitTarget = Robot1_BuyProfit;
   Robots[0].sellChainProfitTarget = Robot1_SellProfit;
   
   Robots[0].buyActive = false;
   Robots[0].sellActive = false;
   Robots[0].buyInLoop = false;
   Robots[0].sellInLoop = false;
   Robots[0].buyTriggered = false;
   Robots[0].sellTriggered = false;
   
   for(int i = 0; i < 10; i++)
   {
      Robots[0].buyLevelUsed[i] = false;
      Robots[0].sellLevelUsed[i] = false;
   }
}

//+------------------------------------------------------------------+
//|              KADEMELİ ROBOT BAŞLAT (ROBOT 2-5)                    |
//+------------------------------------------------------------------+
void InitCascadeRobot(int index)
{
   Robots[index].robotIndex = index;
   Robots[index].buyMagic = Robot1_BuyMagic + (index * 10);
   Robots[index].sellMagic = Robot1_SellMagic + (index * 10);
   
   double distFactor = 1.0;
   double lotFactor = 1.0;
   
   for(int i = 0; i < index; i++)
   {
      distFactor *= (DistancePercent / 100.0);
      lotFactor *= (LotPercent / 100.0);
   }
   
   for(int i = 0; i < 10; i++)
   {
      Robots[index].lots[i] = NormalizeDouble(Robots[0].lots[i] * lotFactor, 2);
      if(Robots[index].lots[i] < 0.01) Robots[index].lots[i] = 0.01;
      
      Robots[index].distances[i] = (int)(Robots[0].distances[i] * distFactor);
      Robots[index].takeProfit[i] = (int)(Robots[0].takeProfit[i] * distFactor);
   }
   
   switch(index)
   {
      case 1:
         Robots[index].buyChainProfitTarget = Robot2_BuyProfit;
         Robots[index].sellChainProfitTarget = Robot2_SellProfit;
         break;
      case 2:
         Robots[index].buyChainProfitTarget = Robot3_BuyProfit;
         Robots[index].sellChainProfitTarget = Robot3_SellProfit;
         break;
      case 3:
         Robots[index].buyChainProfitTarget = Robot4_BuyProfit;
         Robots[index].sellChainProfitTarget = Robot4_SellProfit;
         break;
      case 4:
         Robots[index].buyChainProfitTarget = Robot5_BuyProfit;
         Robots[index].sellChainProfitTarget = Robot5_SellProfit;
         break;
   }
   
   Robots[index].buyActive = false;
   Robots[index].sellActive = false;
   Robots[index].buyInLoop = false;
   Robots[index].sellInLoop = false;
   Robots[index].buyTriggered = false;
   Robots[index].sellTriggered = false;
   
   for(int i = 0; i < 10; i++)
   {
      Robots[index].buyLevelUsed[i] = false;
      Robots[index].sellLevelUsed[i] = false;
   }
}

//+------------------------------------------------------------------+
//|                            DEINIT                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
   DeletePanel();
   Comment("");
}

//+------------------------------------------------------------------+
//|                            ONTICK                                 |
//+------------------------------------------------------------------+
void OnTick()
{
   CheckDailyReset();
   
   bool dailyTargetHit = CheckDailyTarget();
   bool canTrade = IsTradingTime() && !dailyTargetHit;
   
   CheckAllLoops();
   
   for(int i = 0; i < MaxCascadeRobots && i < 5; i++)
   {
      ManageRobot(i, canTrade);
   }
   
   CheckCascadeTriggers();
   UpdatePanel();
   
   // DEBUG - Ekranda görünüyor mu test
   Comment("Test: Robot sistemi çalışıyor - ", TimeToString(TimeCurrent()));
}

//+------------------------------------------------------------------+
//|                    ROBOT YÖNETİMİ                                 |
//+------------------------------------------------------------------+
void ManageRobot(int robotIndex, bool canTrade)
{
   if(TradeDirection == 0 || TradeDirection == 2)
   {
      if(robotIndex == 0)
      {
         if(!Robots[0].buyActive && CountPositions(Robots[0].buyMagic) == 0 && !Robots[0].buyInLoop && canTrade)
         {
            StartRobotBuyChain(0);
         }
      }
      else
      {
         if(Robots[robotIndex].buyTriggered && !Robots[robotIndex].buyActive && 
            CountPositions(Robots[robotIndex].buyMagic) == 0 && !Robots[robotIndex].buyInLoop && canTrade)
         {
            StartRobotBuyChain(robotIndex);
            Robots[robotIndex].buyTriggered = false;
         }
      }
      
      if(Robots[robotIndex].buyActive)
      {
         CheckAndAddMartingale(robotIndex, true);
         UpdateRobotTP(robotIndex, true);
         
         double profit = CalculateRobotProfit(robotIndex, true);
         if(profit >= Robots[robotIndex].buyChainProfitTarget)
         {
            Print("✓ Robot ", robotIndex+1, " BUY hedefine ulaştı! ($", profit, " / $", Robots[robotIndex].buyChainProfitTarget, ")");
            CloseRobotChain(robotIndex, true);
         }
         
         CheckRobotChainCompleted(robotIndex, true);
      }
   }
   
   if(TradeDirection == 1 || TradeDirection == 2)
   {
      if(robotIndex == 0)
      {
         if(!Robots[0].sellActive && CountPositions(Robots[0].sellMagic) == 0 && !Robots[0].sellInLoop && canTrade)
         {
            StartRobotSellChain(0);
         }
      }
      else
      {
         if(Robots[robotIndex].sellTriggered && !Robots[robotIndex].sellActive && 
            CountPositions(Robots[robotIndex].sellMagic) == 0 && !Robots[robotIndex].sellInLoop && canTrade)
         {
            StartRobotSellChain(robotIndex);
            Robots[robotIndex].sellTriggered = false;
         }
      }
      
      if(Robots[robotIndex].sellActive)
      {
         CheckAndAddMartingale(robotIndex, false);
         UpdateRobotTP(robotIndex, false);
         
         double profit = CalculateRobotProfit(robotIndex, false);
         if(profit >= Robots[robotIndex].sellChainProfitTarget)
         {
            Print("✓ Robot ", robotIndex+1, " SELL hedefine ulaştı! ($", profit, " / $", Robots[robotIndex].sellChainProfitTarget, ")");
            CloseRobotChain(robotIndex, false);
         }
         
         CheckRobotChainCompleted(robotIndex, false);
      }
   }
}

//+------------------------------------------------------------------+
//|              SONRAKI ROBOTLARI TETİKLE                            |
//+------------------------------------------------------------------+
void CheckCascadeTriggers()
{
   if(TriggerLevel < 1 || TriggerLevel > 10) return;
   
   int triggerIndex = TriggerLevel - 1;
   
   for(int i = 0; i < MaxCascadeRobots - 1 && i < 4; i++)
   {
      int nextRobot = i + 1;
      
      if(Robots[i].buyActive && Robots[i].buyLevelUsed[triggerIndex] && !Robots[nextRobot].buyTriggered)
      {
         Robots[nextRobot].buyTriggered = true;
         Print("╠═ Robot ", i+1, " K", TriggerLevel, " açtı → Robot ", nextRobot+1, " BUY TETİK!");
      }
      
      if(Robots[i].sellActive && Robots[i].sellLevelUsed[triggerIndex] && !Robots[nextRobot].sellTriggered)
      {
         Robots[nextRobot].sellTriggered = true;
         Print("╠═ Robot ", i+1, " K", TriggerLevel, " açtı → Robot ", nextRobot+1, " SELL TETİK!");
      }
   }
}

//+------------------------------------------------------------------+
//|                  ROBOT ZİNCİR BAŞLAT                              |
//+------------------------------------------------------------------+
void StartRobotBuyChain(int robotIndex)
{
   Robots[robotIndex].buyActive = true;
   for(int i = 0; i < 10; i++)
      Robots[robotIndex].buyLevelUsed[i] = false;
   
   OpenRobotTrade(robotIndex, 0, true);
   Print("╠═ R", robotIndex+1, " BUY başladı (Hedef:$", Robots[robotIndex].buyChainProfitTarget, ")");
}

void StartRobotSellChain(int robotIndex)
{
   Robots[robotIndex].sellActive = true;
   for(int i = 0; i < 10; i++)
      Robots[robotIndex].sellLevelUsed[i] = false;
   
   OpenRobotTrade(robotIndex, 0, false);
   Print("╠═ R", robotIndex+1, " SELL başladı (Hedef:$", Robots[robotIndex].sellChainProfitTarget, ")");
}

//+------------------------------------------------------------------+
//|                    ROBOT İŞLEM AÇ                                 |
//+------------------------------------------------------------------+
void OpenRobotTrade(int robotIndex, int level, bool isBuy)
{
   int magic = isBuy ? Robots[robotIndex].buyMagic : Robots[robotIndex].sellMagic;
   double lot = Robots[robotIndex].lots[level];
   int tpPoints = Robots[robotIndex].takeProfit[level];
   
   double price, tp;
   int orderType;
   color clr;
   string comment = "R" + IntegerToString(robotIndex+1) + (isBuy ? "B" : "S") + "K" + IntegerToString(level+1);
   
   if(isBuy)
   {
      price = Ask;
      tp = price + tpPoints * Point;
      orderType = OP_BUY;
      clr = clrBlue;
   }
   else
   {
      price = Bid;
      tp = price - tpPoints * Point;
      orderType = OP_SELL;
      clr = clrRed;
   }
   
   int ticket = OrderSend(Symbol(), orderType, lot, price, 3, 0, tp, comment, magic, 0, clr);
   
   if(ticket > 0)
   {
      if(isBuy)
         Robots[robotIndex].buyLevelUsed[level] = true;
      else
         Robots[robotIndex].sellLevelUsed[level] = true;
         
      Print("  ✓ R", robotIndex+1, " ", (isBuy ? "BUY" : "SELL"), " K", level+1, " → Lot:", lot, " #", ticket);
   }
   else
   {
      Print("  ✗ R", robotIndex+1, " ", (isBuy ? "BUY" : "SELL"), " K", level+1, " HATA:", GetLastError());
   }
}

//+------------------------------------------------------------------+
//|                ROBOT MARTİNGALE KONTROLÜ                          |
//+------------------------------------------------------------------+
void CheckAndAddMartingale(int robotIndex, bool isBuy)
{
   int magic = isBuy ? Robots[robotIndex].buyMagic : Robots[robotIndex].sellMagic;
   double referencePrice = isBuy ? GetLowestPrice(magic) : GetHighestPrice(magic);
   
   if(referencePrice <= 0) return;
   
   for(int level = 1; level < 10; level++)
   {
      bool levelUsed = isBuy ? Robots[robotIndex].buyLevelUsed[level] : Robots[robotIndex].sellLevelUsed[level];
      if(levelUsed) continue;
      
      double targetPrice;
      bool condition;
      
      if(isBuy)
      {
         targetPrice = referencePrice - Robots[robotIndex].distances[level] * Point;
         condition = (Bid <= targetPrice);
      }
      else
      {
         targetPrice = referencePrice + Robots[robotIndex].distances[level] * Point;
         condition = (Ask >= targetPrice);
      }
      
      if(condition)
      {
         OpenRobotTrade(robotIndex, level, isBuy);
         break;
      }
   }
}

//+------------------------------------------------------------------+
//|                    ROBOT TP GÜNCELLE                              |
//+------------------------------------------------------------------+
void UpdateRobotTP(int robotIndex, bool isBuy)
{
   int magic = isBuy ? Robots[robotIndex].buyMagic : Robots[robotIndex].sellMagic;
   int highestLevel = GetHighestLevel(robotIndex, isBuy);
   
   if(highestLevel < 0) return;
   
   double refPrice = isBuy ? GetHighestPrice(magic) : GetLowestSellPrice(magic);
   if(refPrice <= 0) return;
   
   double newTP;
   if(isBuy)
      newTP = refPrice + Robots[robotIndex].takeProfit[highestLevel] * Point;
   else
      newTP = refPrice - Robots[robotIndex].takeProfit[highestLevel] * Point;
   
   for(int i = 0; i < OrdersTotal(); i++)
   {
      if(OrderSelect(i, SELECT_BY_POS, MODE_TRADES))
      {
         if(OrderMagicNumber() == magic && OrderSymbol() == Symbol())
         {
            if(MathAbs(OrderTakeProfit() - newTP) > Point)
            {
               bool result = OrderModify(OrderTicket(), OrderOpenPrice(), OrderStopLoss(), newTP, 0, isBuy ? clrBlue : clrRed);
               if(!result)
               {
                  int error = GetLastError();
                  if(error != 1 && error != 0) // 1 = ERR_NO_ERROR, 0 = başarılı
                  {
                     Print("TP güncelleme hatası: Ticket #", OrderTicket(), " Error: ", error);
                  }
               }
            }
         }
      }
   }
}

int GetHighestLevel(int robotIndex, bool isBuy)
{
   int highest = -1;
   for(int i = 9; i >= 0; i--)
   {
      bool levelUsed = isBuy ? Robots[robotIndex].buyLevelUsed[i] : Robots[robotIndex].sellLevelUsed[i];
      if(levelUsed)
      {
         highest = i;
         break;
      }
   }
   return highest;
}

double CalculateRobotProfit(int robotIndex, bool isBuy)
{
   int magic = isBuy ? Robots[robotIndex].buyMagic : Robots[robotIndex].sellMagic;
   double profit = 0;
   
   for(int i = 0; i < OrdersTotal(); i++)
   {
      if(OrderSelect(i, SELECT_BY_POS, MODE_TRADES))
      {
         if(OrderMagicNumber() == magic && OrderSymbol() == Symbol())
         {
            profit += OrderProfit() + OrderSwap() + OrderCommission();
         }
      }
   }
   return profit;
}

//+------------------------------------------------------------------+
//|                  ROBOT ZİNCİRİ KAPAT                              |
//+------------------------------------------------------------------+
void CloseRobotChain(int robotIndex, bool isBuy)
{
   int magic = isBuy ? Robots[robotIndex].buyMagic : Robots[robotIndex].sellMagic;
   int closedCount = 0;
   double totalProfit = 0;
   
   for(int i = OrdersTotal() - 1; i >= 0; i--)
   {
      if(OrderSelect(i, SELECT_BY_POS, MODE_TRADES))
      {
         if(OrderMagicNumber() == magic && OrderSymbol() == Symbol())
         {
            double closePrice = isBuy ? Bid : Ask;
            double orderProfit = OrderProfit() + OrderSwap() + OrderCommission();
            
            if(OrderClose(OrderTicket(), OrderLots(), closePrice, 3, isBuy ? clrBlue : clrRed))
            {
               closedCount++;
               totalProfit += orderProfit;
            }
         }
      }
   }
   
   Print("╠═══════════════════════════════════════════════╣");
   Print("  TOPLU KAPAMA: R", robotIndex+1, " ", (isBuy ? "BUY" : "SELL"));
   Print("  İşlem: ", closedCount, " adet | Kar: $", DoubleToString(totalProfit, 2));
   Print("╠═══════════════════════════════════════════════╣");
   
   if(isBuy)
   {
      Robots[robotIndex].buyActive = false;
      Robots[robotIndex].buyInLoop = true;
      Robots[robotIndex].buyLoopEndTime = TimeCurrent() + LoopWaitMinutes * 60;
   }
   else
   {
      Robots[robotIndex].sellActive = false;
      Robots[robotIndex].sellInLoop = true;
      Robots[robotIndex].sellLoopEndTime = TimeCurrent() + LoopWaitMinutes * 60;
   }
}

//+------------------------------------------------------------------+
//|            ROBOT ZİNCİR TAMAMLANMA KONTROLÜ                       |
//+------------------------------------------------------------------+
void CheckRobotChainCompleted(int robotIndex, bool isBuy)
{
   int magic = isBuy ? Robots[robotIndex].buyMagic : Robots[robotIndex].sellMagic;
   int posCount = CountPositions(magic);
   
   if(posCount == 0)
   {
      if(isBuy && Robots[robotIndex].buyActive)
      {
         Robots[robotIndex].buyActive = false;
         Robots[robotIndex].buyInLoop = true;
         Robots[robotIndex].buyLoopEndTime = TimeCurrent() + LoopWaitMinutes * 60;
      }
      else if(!isBuy && Robots[robotIndex].sellActive)
      {
         Robots[robotIndex].sellActive = false;
         Robots[robotIndex].sellInLoop = true;
         Robots[robotIndex].sellLoopEndTime = TimeCurrent() + LoopWaitMinutes * 60;
      }
   }
}

//+------------------------------------------------------------------+
//|                  TÜM DÖNGÜ KONTROLÜ                               |
//+------------------------------------------------------------------+
void CheckAllLoops()
{
   for(int i = 0; i < MaxCascadeRobots && i < 5; i++)
   {
      if(Robots[i].buyInLoop && TimeCurrent() >= Robots[i].buyLoopEndTime)
      {
         Robots[i].buyInLoop = false;
      }
      
      if(Robots[i].sellInLoop && TimeCurrent() >= Robots[i].sellLoopEndTime)
      {
         Robots[i].sellInLoop = false;
      }
   }
}

//+------------------------------------------------------------------+
//|                    POZİSYON SAYISI                                |
//+------------------------------------------------------------------+
int CountPositions(int magic)
{
   int count = 0;
   for(int i = 0; i < OrdersTotal(); i++)
   {
      if(OrderSelect(i, SELECT_BY_POS, MODE_TRADES))
      {
         if(OrderMagicNumber() == magic && OrderSymbol() == Symbol())
            count++;
      }
   }
   return count;
}

//+------------------------------------------------------------------+
//|                    EN DÜŞÜK FİYAT                                 |
//+------------------------------------------------------------------+
double GetLowestPrice(int magic)
{
   double lowest = 0;
   for(int i = 0; i < OrdersTotal(); i++)
   {
      if(OrderSelect(i, SELECT_BY_POS, MODE_TRADES))
      {
         if(OrderMagicNumber() == magic && OrderSymbol() == Symbol() && OrderType() == OP_BUY)
         {
            if(lowest == 0 || OrderOpenPrice() < lowest)
               lowest = OrderOpenPrice();
         }
      }
   }
   return lowest;
}

//+------------------------------------------------------------------+
//|                    EN YÜKSEK FİYAT                                |
//+------------------------------------------------------------------+
double GetHighestPrice(int magic)
{
   double highest = 0;
   for(int i = 0; i < OrdersTotal(); i++)
   {
      if(OrderSelect(i, SELECT_BY_POS, MODE_TRADES))
      {
         if(OrderMagicNumber() == magic && OrderSymbol() == Symbol())
         {
            if(OrderType() == OP_BUY || OrderType() == OP_SELL)
            {
               if(highest == 0 || OrderOpenPrice() > highest)
                  highest = OrderOpenPrice();
            }
         }
      }
   }
   return highest;
}

//+------------------------------------------------------------------+
//|                    EN DÜŞÜK FİYAT (SELL)                          |
//+------------------------------------------------------------------+
double GetLowestSellPrice(int magic)
{
   double lowest = 0;
   for(int i = 0; i < OrdersTotal(); i++)
   {
      if(OrderSelect(i, SELECT_BY_POS, MODE_TRADES))
      {
         if(OrderMagicNumber() == magic && OrderSymbol() == Symbol() && OrderType() == OP_SELL)
         {
            if(lowest == 0 || OrderOpenPrice() < lowest)
               lowest = OrderOpenPrice();
         }
      }
   }
   return lowest;
}

//+------------------------------------------------------------------+
//|                 TİCARET SAATİ KONTROLÜ                            |
//+------------------------------------------------------------------+
bool IsTradingTime()
{
   datetime currentTime = TimeCurrent();
   int hour = TimeHour(currentTime);
   int minute = TimeMinute(currentTime);
   
   int startMinutes = StartHour * 60 + StartMinute;
   int endMinutes = EndHour * 60 + EndMinute;
   int currentMinutes = hour * 60 + minute;
   
   if(startMinutes < endMinutes)
      return (currentMinutes >= startMinutes && currentMinutes < endMinutes);
   else
      return (currentMinutes >= startMinutes || currentMinutes < endMinutes);
}

//+------------------------------------------------------------------+
//|                    GÜNLÜK SIFIRLAMA                               |
//+------------------------------------------------------------------+
void CheckDailyReset()
{
   int currentDay = TimeDay(TimeCurrent());
   
   if(currentDay != LastDay)
   {
      DailyStartBalance = AccountBalance();
      LastDay = currentDay;
      DailyTargetReached = false;
      Print("╠═ YENİ GÜN - GÜNLÜK KAR SIFIRLANDI ═╣");
   }
}

//+------------------------------------------------------------------+
//|                  GÜNLÜK KAR KONTROLÜ                              |
//+------------------------------------------------------------------+
bool CheckDailyTarget()
{
   if(DailyTargetReached) return true;
   
   double currentProfit = AccountBalance() - DailyStartBalance;
   
   if(currentProfit >= DailyProfitTarget)
   {
      DailyTargetReached = true;
      Print("✓✓✓ GÜNLÜK KAR HEDEFİNE ULAŞILDI! ✓✓✓");
      return true;
   }
   
   return false;
}

//+------------------------------------------------------------------+
//|                    PANEL OLUŞTUR                                  |
//+------------------------------------------------------------------+
void CreatePanel()
{
   ArrayResize(panelObjects, 200);
   totalPanelObjects = 0;
}

//+------------------------------------------------------------------+
//|                    PANEL SİL                                      |
//+------------------------------------------------------------------+
void DeletePanel()
{
   for(int i = 0; i < totalPanelObjects; i++)
   {
      ObjectDelete(0, panelObjects[i]);
   }
   ArrayResize(panelObjects, 0);
   totalPanelObjects = 0;
}

//+------------------------------------------------------------------+
//|                    LABEL OLUŞTUR                                  |
//+------------------------------------------------------------------+
void CreateLabel(string name, int x, int y, string text, int size, color clr)
{
   ObjectCreate(0, name, OBJ_LABEL, 0, 0, 0);
   ObjectSetInteger(0, name, OBJPROP_CORNER, CORNER_LEFT_UPPER);
   ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x);
   ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y);
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, size);
   ObjectSetString(0, name, OBJPROP_FONT, "Arial Bold");
   ObjectSetString(0, name, OBJPROP_TEXT, text);
   
   panelObjects[totalPanelObjects] = name;
   totalPanelObjects++;
}

//+------------------------------------------------------------------+
//|                    LABEL GÜNCELLE                                 |
//+------------------------------------------------------------------+
void UpdateLabel(string name, string text, color clr)
{
   ObjectSetString(0, name, OBJPROP_TEXT, text);
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
}

//+------------------------------------------------------------------+
//|                    PANEL GÜNCELLE                                 |
//+------------------------------------------------------------------+
void UpdatePanel()
{
   // Önce eski objeleri sil
   for(int i = 0; i < totalPanelObjects; i++)
   {
      ObjectDelete(0, panelObjects[i]);
   }
   totalPanelObjects = 0;
   
   int yPos = PanelY;
   
   // BAŞLIK
   CreateLabel("Header", PanelX, yPos, "═══ KADEMELİ ROBOT SİSTEMİ v6.0 ═══", HeaderSize, clrGold);
   yPos += HeaderSize + 10;
   
   // SİSTEM DURUMU
   string status = IsTradingTime() ? "✓ AKTİF" : "✗ KAPALI";
   color statusColor = IsTradingTime() ? clrLime : clrRed;
   CreateLabel("Status", PanelX, yPos, "Durum: " + status, RobotSize, statusColor);
   yPos += RobotSize + 10;
   
   // GÜNLÜK KAR
   double dailyProfit = AccountBalance() - DailyStartBalance;
   color profitColor = dailyProfit >= 0 ? clrLime : clrRed;
   CreateLabel("DailyProfit", PanelX, yPos, "GÜNLÜK KAR: $" + DoubleToString(dailyProfit, 2) + " / $" + DoubleToString(DailyProfitTarget, 2), RobotSize, profitColor);
   yPos += RobotSize + 15;
   
   // AYRİM ÇİZGİSİ
   CreateLabel("Sep1", PanelX, yPos, "════════════════════════════════════════", DetailSize, clrDarkGray);
   yPos += DetailSize + 10;
   
   // HER ROBOT İÇİN DETAYLI BİLGİ
   for(int i = 0; i < MaxCascadeRobots && i < 5; i++)
   {
      // ROBOT BAŞLIĞI
      CreateLabel("R" + IntegerToString(i) + "_Title", PanelX, yPos, "╔═══ ROBOT " + IntegerToString(i+1) + " ═══╗", RobotSize, clrAqua);
      yPos += RobotSize + 8;
      
      // BUY BİLGİLERİ
      DisplayRobotSide(i, true, PanelX + 10, yPos);
      
      // SELL BİLGİLERİ
      DisplayRobotSide(i, false, PanelX + 10, yPos);
      
      // AYRİM ÇİZGİSİ
      if(i < MaxCascadeRobots - 1)
      {
         CreateLabel("Sep" + IntegerToString(i+2), PanelX, yPos, "────────────────────────────────────────", DetailSize, clrDarkGray);
         yPos += DetailSize + 8;
      }
   }
   
   // ALT BİLGİ
   yPos += 5;
   CreateLabel("Footer", PanelX, yPos, "═══════════════════════════════════════", DetailSize, clrDarkGray);
   yPos += DetailSize + 5;
   
   datetime serverTime = TimeCurrent();
   string timeStr = TimeToString(serverTime, TIME_DATE|TIME_MINUTES);
   CreateLabel("Time", PanelX, yPos, "Sunucu: " + timeStr, DetailSize - 1, clrSilver);
   
   ChartRedraw();
}

//+------------------------------------------------------------------+
//|                 ROBOT TARAF BİLGİSİ GÖSTER                        |
//+------------------------------------------------------------------+
void DisplayRobotSide(int robotIndex, bool isBuy, int x, int &yPos)
{
   string side = isBuy ? "BUY" : "SELL";
   string prefix = "R" + IntegerToString(robotIndex) + (isBuy ? "B" : "S");
   color sideColor = isBuy ? clrDodgerBlue : clrOrangeRed;
   
   bool isActive = isBuy ? Robots[robotIndex].buyActive : Robots[robotIndex].sellActive;
   bool inLoop = isBuy ? Robots[robotIndex].buyInLoop : Robots[robotIndex].sellInLoop;
   bool triggered = isBuy ? Robots[robotIndex].buyTriggered : Robots[robotIndex].sellTriggered;
   
   // TARAF BAŞLIĞI
   CreateLabel(prefix + "_Side", x, yPos, "▶ " + side, DetailSize + 1, sideColor);
   yPos += DetailSize + 5;
   
   if(isActive)
   {
      // AKTİF KADEME SAYISI
      int activeCount = 0;
      for(int j = 0; j < 10; j++)
      {
         bool levelUsed = isBuy ? Robots[robotIndex].buyLevelUsed[j] : Robots[robotIndex].sellLevelUsed[j];
         if(levelUsed) activeCount++;
      }
      
      // KAR DURUMU
      double profit = CalculateRobotProfit(robotIndex, isBuy);
      double target = isBuy ? Robots[robotIndex].buyChainProfitTarget : Robots[robotIndex].sellChainProfitTarget;
      color profitColor = profit >= target * 0.8 ? clrLime : (profit >= target * 0.5 ? clrYellow : clrWhite);
      
      CreateLabel(prefix + "_Info", x + 15, yPos, "Kademe: " + IntegerToString(activeCount) + "/10", DetailSize, clrWhite);
      yPos += DetailSize + 5;
      
      CreateLabel(prefix + "_Profit", x + 15, yPos, "Kar: $" + DoubleToString(profit, 2) + " / $" + DoubleToString(target, 2), DetailSize, profitColor);
      yPos += DetailSize + 5;
   }
   else if(inLoop)
   {
      datetime loopEnd = isBuy ? Robots[robotIndex].buyLoopEndTime : Robots[robotIndex].sellLoopEndTime;
      int remaining = (int)((loopEnd - TimeCurrent()) / 60);
      
      CreateLabel(prefix + "_Info", x + 15, yPos, "Durum: DÖNGÜ BEKLİYOR", DetailSize, clrOrange);
      yPos += DetailSize + 5;
      
      CreateLabel(prefix + "_Time", x + 15, yPos, "Kalan: " + IntegerToString(remaining) + " dakika", DetailSize, clrYellow);
      yPos += DetailSize + 5;
   }
   else if(triggered)
   {
      CreateLabel(prefix + "_Info", x + 15, yPos, "Durum: TETİKLENDİ ⏰", DetailSize, clrYellow);
      yPos += DetailSize + 5;
      
      CreateLabel(prefix + "_Wait", x + 15, yPos, "İşlem açmak için bekliyor...", DetailSize, clrGray);
      yPos += DetailSize + 5;
   }
   else
   {
      CreateLabel(prefix + "_Info", x + 15, yPos, "Durum: BEKLEMEDE", DetailSize, clrGray);
      yPos += DetailSize + 5;
      
      CreateLabel(prefix + "_Ready", x + 15, yPos, "Hazır", DetailSize, clrDarkGray);
      yPos += DetailSize + 5;
   }
}

//+------------------------------------------------------------------+