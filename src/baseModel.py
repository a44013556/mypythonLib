from abc import ABC, abstractmethod
from typing import List, Tuple, Any, Optional, Dict


"""
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

概要: 汎用テーブルに関するクラスを定義

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""
class IDatabaseEngine(ABC):
    @abstractmethod
    def select_one(self, query: str, params: list) -> Optional[Dict[str,Any]]:
        pass

    @abstractmethod
    def select_all(self, query: str, params: list) -> List[Dict[str,Any]]:
        pass

    @abstractmethod
    def execute(self, query: str, params: list) -> int:
        pass



class BaseModel():
  
    tableName = ""
    _engine: Optional[IDatabaseEngine] = None

    @classmethod
    def set_engine(cls, engine:IDatabaseEngine):
        cls._engine = engine
    
    @classmethod
    def _get_engine(cls):
        if cls._engine is None:
            raise RuntimeError("Database Engine is not set. Please use the set_engine method to set the Engine")
        return cls._engine

    @classmethod
    def commonSelectSingle(cls, conditions: list, conditionsValues: list,cols = None ) -> Optional[Dict[str, Any]]:
        """
        テーブルから一件だけ取得する
        conditions:条件の項目,Sizeは2のListになり、最初は項目、二つ目は演算子になる、もしsizeは1になったら、=になる
        conditionsValues:条件の値
        cols:欲しい項目になり、defaultはNone, もしNoneの場合、全項目になる
        """
        
        colsStmt = ",".join(cols) if cols else "*"
        conditionsStmt = cls._buildConditionsStmt(conditions)
        query = f"SELECT {colsStmt} FROM {cls.tableName} WHERE {conditionsStmt}"
        # クエリを実行
        return cls._get_engine().select_one(query, conditionsValues)
        
    @classmethod
    def commonSelect(cls, conditions: list, conditionsValues: list,cols = None ,limit = None, order = None, reverse = False) -> Optional[List[Dict[str, Any]]]:
        """
        テーブルから複数件取得する
        conditions:条件の項目,Sizeは2のListになり、最初は項目、二つ目は演算子になる、もしsizeは1になったら、=になる
        conditionsValues:条件の値
        cols:欲しい項目になり、defaultはNone, もしNoneの場合、全項目になる
        limit:表示件数、もしNoneの場合、全件になる
        order:オーダー順
        reverse: Trueの場合、降順になる
        """
        
        conditionsStmt = cls._buildConditionsStmt(conditions)
        colsStmt = ",".join(cols) if cols else "*"
        limitStmt =  f"LIMIT {limit}" if limit else ""
        orderStmt = "ORDER BY " + ",".join(order) if order else ""
        if reverse and orderStmt:
            orderStmt += " DESC"
        query = f'''SELECT {colsStmt} FROM {cls.tableName} WHERE {conditionsStmt} {orderStmt} {limitStmt}'''
        # クエリを実行
        return cls._get_engine().select_all(query, conditionsValues)
    
    @classmethod
    def commonDelete(cls, conditions: list, conditionsValues: list):
        """
        テーブルからレコードを削除する
        conditions:条件の項目,Sizeは2のListになり、最初は項目、二つ目は演算子になる、もしsizeは1になったら、=になる
        conditionsValues:条件の値
        """
        conditionsStmt = cls._buildConditionsStmt(conditions)
        query = f'''DELETE FROM {cls.tableName} WHERE {conditionsStmt}'''
        return cls._get_engine().execute(query, conditionsValues)
    
    @classmethod
    def commonInsert(cls, valuesCols, values):
        """
        テーブルからレコードを削除する
        valuesCols:対象項目
        values:対象値
        """
        valuesColsStmt = ",".join(valuesCols)
        valuesValuesStmt = ",".join(["%s"] * len(valuesCols))
        
        query = f'''INSERT INTO {cls.tableName} ( {valuesColsStmt} ) VALUES ( {valuesValuesStmt} )'''

        return cls._get_engine().execute(query, values)
    
    @classmethod
    def _buildConditionsStmt(cls, conditions):
        """
        条件文を作成する
        conditions:条件の項目,Sizeは2のListになり、最初は項目、二つ目は演算子になる、もしsizeは1になったら、=になる
        """
        
        return " AND ".join([c[0] + " " + (c[1] if len(c) > 1 else "=") + " %s" for c in conditions])