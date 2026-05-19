import os
import json
from datetime import datetime

SAVE_DIR = "saves"

def init_save_dir():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

def get_save_slots():
    init_save_dir()
    slots = []
    for i in range(1, 5):
        path = os.path.join(SAVE_DIR, f"slot_{i}.json")
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                    slots.append({
                        "slot": i, "empty": False,
                        "date": data.get("save_date", "Unknown"),
                        "cash": data.get("player", {}).get("cash", 0)
                    })
            except:
                slots.append({"slot": i, "empty": True})
        else:
            slots.append({"slot": i, "empty": True})
    return slots

def save_game(slot, player, game_clock, game, active_staff, owned_items, placed_props, current_desk_id, current_wall_id, hours_until_audit):
    init_save_dir()
    
    stock_data = {}
    for s in game.stocks:
        stock_data[s.name] = {
            "price": s.price,
            "history": s.history[-200:] if hasattr(s, 'history') else []
        }
        
    staff_data = []
    for emp_id, emp in active_staff.items():
        staff_data.append({
            "id": emp_id, "energy": emp.energy,
            "role": getattr(emp, 'role', 'Salesman'),
            "config": emp.config
        })
        
    data = {
        "save_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "player": {
            "cash": player.cash,
            "portfolio": getattr(player, 'portfolio', {}),
            "shorts": getattr(player, 'shorts', {}), # Saves your shorts!
            "cost_basis": getattr(player, 'cost_basis', {}),
            "trade_history": getattr(player, 'trade_history', []),
            "offshore": getattr(player, 'offshore', 0),
            "owed_taxes": getattr(player, 'owed_taxes', 0),
            "taxable_profit": getattr(player, 'taxable_profit', 0),
            "hidden_profit": getattr(player, 'hidden_profit', 0),
            "audit_starting_profit": getattr(player, 'audit_starting_profit', 0)
        },
        "clock": {"day": game_clock.current_time.day, "hour": game_clock.current_time.hour, "minute": game_clock.current_time.minute},
        "hours_until_audit": hours_until_audit,
        "shop": {"owned_items": owned_items, "placed_props": placed_props, "equipped_desk": current_desk_id, "equipped_wall": current_wall_id},
        "staff": staff_data,
        "stocks": stock_data
    }
    
    with open(os.path.join(SAVE_DIR, f"slot_{slot}.json"), "w") as f:
        json.dump(data, f, indent=4)

def load_game_data(slot):
    path = os.path.join(SAVE_DIR, f"slot_{slot}.json")
    if os.path.exists(path):
        with open(path, "r") as f: return json.load(f)
    return None