
from sklearn import datasets
import numpy as np
import matplotlib.pyplot as plt
# from .model_plot import SVM_Plot

def Grid_Search_CV(model, param_grid, X,y, cv=5):
    from sklearn.model_selection import GridSearchCV
    return GridSearchCV(model, param_grid, cv=cv).fit(X, y)



def plot_decision_boundaries(X,y, clf, title=None):
    def make_meshgrid(x, y, h=.02):
        x_min, x_max = x.min() - 1, x.max() + 1
        y_min, y_max = y.min() - 1, y.max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))
        return xx, yy

    def plot_contours(ax, clf, xx, yy, **params):
        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        out = ax.contourf(xx, yy, Z, **params)
        return out

    fig, ax = plt.subplots()
    # title for the plots
    if title == None:
        title = clf.__class__.__name__
    # Set-up grid for plotting.
    X0, X1 = X[:, 0], X[:, 1]
    xx, yy = make_meshgrid(X0, X1)

    plot_contours(ax, clf, xx, yy, cmap=plt.cm.coolwarm, alpha=0.8)
    ax.scatter(X0, X1,c=y ,cmap=plt.cm.coolwarm, s=20, edgecolors='k')
    ax.set_ylabel('y label here')
    ax.set_xlabel('x label here')
    ax.set_xticks(())
    ax.set_yticks(())
    ax.set_title(title)
    ax.legend()
    plt.show()





def plot_Polyn(X,y,clf):
    X = X[0]
    plt.figure(figsize=(10, 6))
    plt.title("Your first polynomial regression – congrats! :)", size=16)
    plt.scatter(X, y)
    plt.plot(X, clf.predict(X), c="red")
    plt.show()


class models():

    class Regression: 
        def param_grid(model_name: str, Grid_Search=False):
            match model_name:
                case "Logistic_Regression":
                    param_grid = [{'C': [0.001, 0.01, 0.1, 1, 10, 100]}]
                case "Elastic_Net":
                    param_grid = [
                        {
                            "alpha": [0, 0.0001, 0.001, 0.01, 0.1, 0.3, 0.5, 0.7, 1, 10, 100],
                        }
                    ]
                case "Polynomial_Regression":
                    param_grid = [
                        {"poly_features__degree": [1, 2, 3, 4, 5], }
                    ]
            return param_grid

        def Linear_Regression(self, Grid_Search=False):
            from sklearn.linear_model import LinearRegression
            return LinearRegression()

        def Logistic_Regression(self,C=1, Grid_Search=False):
            from sklearn.linear_model import LogisticRegression
            if Grid_Search:
                return Grid_Search_CV(LogisticRegression(), self.param_grid("Logistic_Regression"))
            return LogisticRegression()

        def Polynomial_Regression(self, degree=2, Grid_Search=False):
            from sklearn.preprocessing import PolynomialFeatures
            from sklearn.linear_model import LinearRegression
            from sklearn.pipeline import Pipeline

            model = Pipeline([
                ("poly_features", PolynomialFeatures(degree=int(degree))),
                ("svm_clf", LinearRegression())
            ])
            if Grid_Search:
                return Grid_Search_CV(model, self.param_grid("Polynomial_Regression"))

            return model

        def Elastic_Net(self,alpha=1, Grid_Search=False):
            from sklearn.linear_model import ElasticNet
            if Grid_Search:
                return Grid_Search_CV(ElasticNet(), self.param_grid("Elastic_Net"))
            return ElasticNet(alpha=float(alpha))

    class Trees:
        def param_grid(model_name: str):
            match model_name:
                case "Decision_Tree":
                    param_grid = [
                        {'criterion': ['gini', 'entropy']},
                    ]
                # case "Regressor_Tree":
                #     param_grid = [
                #         {'criterion': [
                #             'squared_error', 'friedman_mse', 'absolute_error', 'poisson']},
                #     ]
            return param_grid

        def Decision_Tree(self, criterion="gini", Grid_Search=False):
            from sklearn.tree import DecisionTreeClassifier
            if Grid_Search:
                return Grid_Search_CV(DecisionTreeClassifier(), self.param_grid("Decision_Tree"))

            return DecisionTreeClassifier(criterion=criterion)

        def Regressor_Tree(self, Grid_Search=False):
            from sklearn.tree import DecisionTreeRegressor
            if Grid_Search:
                return Grid_Search_CV(DecisionTreeRegressor(), self.param_grid("Regressor_Tree"))

            return DecisionTreeRegressor()

    class Ensemble_Learning:
        def param_grid(model_name: str):
            match model_name:
                case "Random_Forest":
                    param_grid = [
                        {'n_estimators': [1, 10, 30, 50,
                                          70, 100, 120, 150, 200, 500]},
                    ]
                case "Extra_Trees":
                    param_grid = [
                        {'n_estimators': [1, 10, 30, 50,
                                          70, 100, 120, 150, 200, 500]}
                    ]

                case "Ada_Boost":
                    param_grid = [
                        {'n_estimators': [1, 10, 30, 50,
                                          70, 100, 120, 150, 200, 500]},
                        {'learning_rate': [0.1, 0.2, 0.3,
                                           0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]},
                    ]

                case "Gradient_Boosting":
                    param_grid = [
                        {'n_estimators': [1, 10, 30, 50,
                                          70, 100, 120, 150, 200, 500]},
                        {'learning_rate': [0.1, 0.2, 0.3,
                                           0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]},
                    ]
            return param_grid

        def Voting_Classifiers(self):
            pass

        def Random_Forest_Classifier(self,n_estimators=100,  Grid_Search=False):
            from sklearn.ensemble import RandomForestClassifier
            if Grid_Search:
                return Grid_Search_CV(RandomForestClassifier(n_jobs=-1), self.param_grid("Random_Forest"))
            return RandomForestClassifier(n_estimators=int(n_estimators), n_jobs=-1)

        def Random_Forest_Regressor(self,n_estimators=100, Grid_Search=False):
            from sklearn.ensemble import RandomForestRegressor
            if Grid_Search:
                return Grid_Search_CV(RandomForestRegressor(n_jobs=-1), self.param_grid("Random_Forest"))
            return RandomForestRegressor(n_estimators=int(n_estimators),n_jobs=-1)

        def Extra_Trees_Classifier(self,n_estimators=100,  Grid_Search=False):
            from sklearn.ensemble import ExtraTreesClassifier
            if Grid_Search:
                return Grid_Search_CV(ExtraTreesClassifier(n_jobs=-1), self.param_grid("Extra_Trees"))

            return ExtraTreesClassifier(n_estimators=int(n_estimators), n_jobs=-1)

        def Extra_Trees_Regressor(self,n_estimators=100, Grid_Search=False):
            from sklearn.ensemble import ExtraTreesRegressor
            if Grid_Search:
                return Grid_Search_CV(ExtraTreesRegressor(n_jobs=-1), self.param_grid("Extra_Trees"))

            return ExtraTreesRegressor(n_estimators=int(n_estimators),n_jobs=-1)

        def Ada_Boost_Classifier(self,n_estimators=50,learning_rate=1, Grid_Search=False):
            from sklearn.ensemble import AdaBoostClassifier
            from sklearn.tree import DecisionTreeClassifier

            if Grid_Search:
                return Grid_Search_CV(AdaBoostClassifier(DecisionTreeClassifier(max_depth=1)), self.param_grid("Ada_Boost"))
            return AdaBoostClassifier(DecisionTreeClassifier(max_depth=1),n_estimators=int(n_estimators),learning_rate=float(learning_rate), algorithm="SAMME.R")

        def Ada_Boost_Regressor(self,n_estimators=50,learning_rate=1, Grid_Search=False):
            from sklearn.ensemble import AdaBoostRegressor
            from sklearn.tree import DecisionTreeRegressor

            if Grid_Search:
                return Grid_Search_CV(AdaBoostRegressor(DecisionTreeRegressor(max_depth=1)), self.param_grid("Ada_Boost"))
            return AdaBoostRegressor(DecisionTreeRegressor(max_depth=1),n_estimators=int(n_estimators),learning_rate=float(learning_rate))

        def Gradient_Boosting_Classifier(self,n_estimators=100,learning_rate=0.1, Grid_Search=False):
            from sklearn.ensemble import GradientBoostingClassifier
            if Grid_Search:
                return Grid_Search_CV(GradientBoostingClassifier(), self.param_grid("Gradient_Boosting"))
            return GradientBoostingClassifier(n_estimators=int(n_estimators),learning_rate=float(learning_rate))

        def Gradient_Boosting_Regressor(self,n_estimators=100,learning_rate=0.1, Grid_Search=False):
            from sklearn.ensemble import GradientBoostingRegressor
            if Grid_Search:
                return Grid_Search_CV(GradientBoostingRegressor(), self.param_grid("Gradient_Boosting"))
            return GradientBoostingRegressor(n_estimators=int(n_estimators),learning_rate=float(learning_rate))

    class SVM:
        def param_grid(self, model_name: str):
            match model_name:
                case "LinearSVM":
                    param_grid = [
                        {'svm_clf__C': [0.1, 1, 10, 100, 1000]},
                    ]
                case "nonLinearSVM":
                    param_grid = [
                        {'svm_clf__C': [0.1, 1, 10, 100, 1000],
                         'svm_clf__gamma': [1, 0.1, 0.01, 0.001, 0.0001, 'auto']},
                    ]
            return param_grid

        def LinearSVM(self, Grid_Search=False):
            from sklearn.svm import LinearSVC
            from sklearn.pipeline import Pipeline
            from sklearn.preprocessing import StandardScaler

            model = Pipeline([
                ("scaler", StandardScaler()),
                ("svm_clf", LinearSVC())
            ])
            if Grid_Search:
                return Grid_Search_CV(model, self.param_grid("LinearSVM"))

            return model

        def nonLinearSVM_ploy(self,C=1,gamma="scale", Grid_Search=False):
            from sklearn.svm import SVC
            from sklearn.pipeline import Pipeline
            from sklearn.preprocessing import StandardScaler

            try :
                gamma = float(gamma)
            except :
                pass
            model = Pipeline([
                ("scaler", StandardScaler()),
                ("svm_clf", SVC(kernel="poly",C=float(C),gamma=gamma))
            ])
            if Grid_Search:
                return Grid_Search_CV(model, self.param_grid("nonLinearSVM"))

            return model

        def nonLinearSVM_rbf(self,C=1,gamma="scale", Grid_Search=False):
            from sklearn.svm import SVC
            from sklearn.pipeline import Pipeline
            from sklearn.preprocessing import StandardScaler
            try :
                gamma = float(gamma)
            except :
                pass
            model = Pipeline([
                ("scaler", StandardScaler()),
                ("svm_clf", SVC(kernel="rbf",C=float(C),gamma=gamma))
            ])
            if Grid_Search:
                return Grid_Search_CV(model, self.param_grid("nonLinearSVM"))

            return model


