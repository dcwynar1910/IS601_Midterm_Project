from dataclasses import dataclass, field
import datetime
from app.calculation import Calculation

@dataclass
class CalculatorMemento:
    history: list
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

    def to_dict(self):
        data = []

        for i in self.history:
            data.append(i.to_dict())

        return {"history": data, "timestamp":self.timestamp.isoformat()}
    
    @classmethod
    def from_dict(cls, data):
        to_list = []

        for i in data["history"]:
            to_list.append(Calculation.from_dict(i))

        return cls(history=to_list, timestamp=datetime.datetime.fromisoformat((data['timestamp'])))