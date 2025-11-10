#!/usr/bin/env python3
"""
Deploy EA to MT4/MT5 Account
Quick script to connect and deploy SmartMartingale EA
"""
import MetaTrader5 as mt5
import sys
from pathlib import Path

# Configuration
ACCOUNT_NUMBER = 123456  # Your Tickmill demo account
PASSWORD = "your_password"  # Your password
SERVER = "Tickmill-Demo"  # Server name
EA_FILE = "SmartMartingale_Pro_v6.ex4"  # EA file
SYMBOL = "EURUSD"
TIMEFRAME = mt5.TIMEFRAME_M15
MAGIC_NUMBER = 10001


def connect_to_mt4():
    """Connect to MT4 terminal"""
    print("🔌 Connecting to MT4...")

    if not mt5.initialize():
        print(f"❌ MT4 initialize failed: {mt5.last_error()}")
        return False

    # Login to account
    authorized = mt5.login(
        login=ACCOUNT_NUMBER,
        password=PASSWORD,
        server=SERVER
    )

    if not authorized:
        print(f"❌ Login failed: {mt5.last_error()}")
        mt5.shutdown()
        return False

    # Get account info
    account_info = mt5.account_info()
    if account_info is None:
        print(f"❌ Failed to get account info")
        mt5.shutdown()
        return False

    print(f"✅ Connected to {SERVER}")
    print(f"📊 Account: {account_info.login}")
    print(f"💰 Balance: ${account_info.balance}")
    print(f"💵 Equity: ${account_info.equity}")

    return True


def deploy_ea():
    """Deploy EA to chart"""
    print(f"\n🚀 Deploying EA to {SYMBOL} {TIMEFRAME}...")

    # Enable symbol
    if not mt5.symbol_select(SYMBOL, True):
        print(f"❌ Failed to select symbol {SYMBOL}")
        return False

    # Get symbol info
    symbol_info = mt5.symbol_info(SYMBOL)
    if symbol_info is None:
        print(f"❌ Symbol {SYMBOL} not found")
        return False

    print(f"✅ Symbol {SYMBOL} ready")
    print(f"   Bid: {symbol_info.bid}")
    print(f"   Ask: {symbol_info.ask}")
    print(f"   Spread: {symbol_info.spread}")

    print("\n⚠️  Manual Steps Required:")
    print("1. In MT4, drag SmartMartingale_Pro_v6.ex4 from Navigator to EURUSD M15 chart")
    print("2. Set magic numbers: BUY=10001, SELL=10002")
    print("3. Enable AutoTrading (F7)")
    print("4. Monitor the dashboard at http://localhost:3000/dashboard")

    return True


def main():
    """Main function"""
    print("═══════════════════════════════════════════════")
    print("   MT Expert Optimizer - EA Deployment")
    print("═══════════════════════════════════════════════\n")

    try:
        if not connect_to_mt4():
            sys.exit(1)

        if not deploy_ea():
            sys.exit(1)

        print("\n✅ Deployment process completed!")
        print("\n📊 Open the dashboard to monitor:")
        print("   http://localhost:3000/dashboard")

        input("\nPress Enter to disconnect...")

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        mt5.shutdown()
        print("\n👋 Disconnected from MT4")


if __name__ == "__main__":
    main()
