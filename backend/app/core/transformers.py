from sklearn.base import BaseEstimator, TransformerMixin

class ColumnSelector(BaseEstimator, TransformerMixin):
  def __init__(self, columns_to_select):
    self.columns_to_select = columns_to_select

  def fit(self, X, y=None):
    return self

  def transform(self,X):
    return X[self.columns_to_select]