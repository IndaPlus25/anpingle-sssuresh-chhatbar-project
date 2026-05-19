class Player:
    def __init__(self, name):
        self.name = name
        self.cash = 1000000000
        self.portfolio = {}
        self.shorts = {}  # {stock_name: {"qty": int, "entry_price": float}}
        self.x = 300
        self.y = 200
        self.direction = "south"
        self.is_moving = False

    def buy_stock(self, stock_name, price, amount):
        """Buys shares of a stock if the player can afford it.
        Returns True if the purchase was successful, False otherwise.
        """
        total_cost = amount * price
        if self.cash >= total_cost:
            self.cash -= total_cost
            if stock_name not in self.portfolio:
                self.portfolio[stock_name] = 0
            self.portfolio[stock_name] += amount
            return True
        return False

    def short_stock(self, stock_name, price, amount):
        """Opens or adds to a short position.
        Player receives cash upfront equal to amount * price.
        Uses weighted average entry price when adding to an existing short.
        """
        self.cash += amount * price
        if stock_name not in self.shorts:
            self.shorts[stock_name] = {"qty": 0, "entry_price": 0.0}
        existing = self.shorts[stock_name]
        total_qty = existing["qty"] + amount
        if total_qty > 0:
            existing["entry_price"] = (
                (existing["entry_price"] * existing["qty"]) + (price * amount)
            ) / total_qty
        existing["qty"] = total_qty

    def settle_shorts(self, current_stocks, prev_prices):
        """Settles P&L for all active short positions after a price tick.
        Stock goes up → player loses money. Stock goes down → player gains money.
        Triggers a margin call (forcibly closes the short) if cash goes negative.
        """
        to_remove = []
        for stock in current_stocks:
            if stock.name in self.shorts:
                short_pos = self.shorts[stock.name]
                if short_pos["qty"] > 0:
                    old_price = prev_prices.get(stock.name, stock.price)
                    price_change = stock.price - old_price
                    self.cash += -price_change * short_pos["qty"]
                    if self.cash < 0:
                        to_remove.append(stock.name)
        for name in to_remove:
            del self.shorts[name]

    def close_long_position(self, stock_name, current_price):
        """Closes an entire long position, selling all shares at current_price.
        Returns (shares_sold, realized_pnl) or (0, 0) if no position found.
        """
        shares = self.portfolio.get(stock_name, 0)
        if shares <= 0:
            return 0, 0
        avg_cost = self.cost_basis.get(stock_name, current_price) if hasattr(self, 'cost_basis') else current_price
        proceeds = shares * current_price
        realized_pnl = proceeds - (shares * avg_cost)
        self.cash += proceeds
        del self.portfolio[stock_name]
        if hasattr(self, 'cost_basis') and stock_name in self.cost_basis:
            del self.cost_basis[stock_name]
        if not hasattr(self, 'taxable_profit'):
            self.taxable_profit = 0
        self.taxable_profit += realized_pnl
        return shares, realized_pnl

    def close_short_position(self, stock_name, current_price):
        """Closes an entire short position, buying back all shares at current_price.
        Returns (shares_closed, realized_pnl) or (0, 0) if no position found.
        """
        if stock_name not in self.shorts:
            return 0, 0
        pos = self.shorts[stock_name]
        qty = pos["qty"]
        if qty <= 0:
            return 0, 0
        entry_price = pos["entry_price"]
        realized_pnl = (entry_price - current_price) * qty
        buyback_cost = qty * current_price
        self.cash -= buyback_cost
        del self.shorts[stock_name]
        if not hasattr(self, 'taxable_profit'):
            self.taxable_profit = 0
        self.taxable_profit += realized_pnl
        return qty, realized_pnl

    def move(self, dx, dy, max_w, max_h):
        if dx != 0 or dy != 0:
            self.is_moving = True
            self.x += dx
            self.y += dy
            
            self.x = max(0, min(self.x, max_w - 40))
            self.y = max(0, min(self.y, max_h - 40))
            
            
            dirs = []
            if dy < 0: dirs.append("north")
            elif dy > 0: dirs.append("south")
            if dx > 0: dirs.append("east")
            elif dx < 0: dirs.append("west")
            self.direction = "".join(dirs)
        else:
            self.is_moving = False