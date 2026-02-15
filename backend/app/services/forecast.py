"""
产量预测服务模块
使用多种机器学习算法进行作物产量预测
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import json


@dataclass
class ForecastResult:
    """预测结果数据结构"""
    predicted_value: float          # 预测值
    confidence_interval: Tuple[float, float]  # 置信区间 (下限, 上限)
    confidence_level: float         # 置信度 (0-1)
    trend: str                      # 趋势: 'up', 'down', 'stable'
    contributing_factors: Dict[str, float]  # 影响因素权重


class MovingAveragePredictor:
    """
    移动平均预测器
    适用于短期预测，计算简单，适合数据量较少的情况
    """

    def __init__(self, window: int = 3):
        self.window = window
        self.history_data = []

    def fit(self, data: List[float]) -> None:
        """拟合历史数据"""
        self.history_data = data

    def predict(self, steps: int = 1) -> List[float]:
        """预测未来 steps 期"""
        if len(self.history_data) < self.window:
            # 数据不足时使用简单平均
            avg = np.mean(self.history_data) if self.history_data else 0
            return [avg] * steps

        predictions = []
        recent_data = self.history_data.copy()

        for _ in range(steps):
            # 计算移动平均
            ma = np.mean(recent_data[-self.window:])
            predictions.append(ma)
            recent_data.append(ma)

        return predictions


class ExponentialSmoothingPredictor:
    """
    指数平滑预测器
    对近期数据赋予更高权重，适用于有趋势的数据
    """

    def __init__(self, alpha: float = 0.3, beta: float = 0.1):
        """
        alpha: 平滑系数 (0-1)，越大则近期数据权重越高
        beta: 趋势平滑系数
        """
        self.alpha = alpha
        self.beta = beta
        self.level = None
        self.trend = None

    def fit(self, data: List[float]) -> None:
        """拟合历史数据，计算初始水平和趋势"""
        if len(data) < 2:
            self.level = data[0] if data else 0
            self.trend = 0
            return

        # 初始化
        self.level = data[0]
        self.trend = data[1] - data[0]

        # 迭代更新
        for i in range(1, len(data)):
            prev_level = self.level
            # 更新水平
            self.level = self.alpha * data[i] + (1 - self.alpha) * (prev_level + self.trend)
            # 更新趋势
            self.trend = self.beta * (self.level - prev_level) + (1 - self.beta) * self.trend

    def predict(self, steps: int = 1) -> List[float]:
        """预测未来 steps 期"""
        if self.level is None:
            return [0] * steps

        predictions = []
        for h in range(1, steps + 1):
            forecast = self.level + h * self.trend
            predictions.append(max(0, forecast))  # 产量不能为负

        return predictions


class SeasonalPredictor:
    """
    季节性预测器
    适用于有明显季节性规律的农业数据
    """

    def __init__(self, season_length: int = 12):
        """
        season_length: 季节周期长度（月度数据为12，季度数据为4）
        """
        self.season_length = season_length
        self.seasonal_indices = []
        self.deseasonalized_trend = []
        self.avg_trend = 0

    def fit(self, data: List[float]) -> None:
        """拟合历史数据，计算季节性指数"""
        if len(data) < self.season_length:
            # 数据不足一个周期，退化为简单平均
            self.avg_trend = np.mean(data) if data else 0
            self.seasonal_indices = [1.0] * self.season_length
            return

        # 计算移动平均（中心化）
        ma_values = []
        half_period = self.season_length // 2

        for i in range(half_period, len(data) - half_period):
            window = data[i - half_period:i + half_period + 1]
            ma_values.append(np.mean(window))

        # 计算季节性比率
        seasonal_ratios = [[] for _ in range(self.season_length)]

        for i, ma in enumerate(ma_values):
            actual_idx = i + half_period
            if actual_idx < len(data):
                season_idx = actual_idx % self.season_length
                ratio = data[actual_idx] / ma if ma != 0 else 1
                seasonal_ratios[season_idx].append(ratio)

        # 计算平均季节性指数
        self.seasonal_indices = []
        for ratios in seasonal_ratios:
            if ratios:
                # 去除异常值后取平均
                filtered = [r for r in ratios if 0.5 < r < 2.0]
                avg_ratio = np.mean(filtered) if filtered else 1.0
                self.seasonal_indices.append(avg_ratio)
            else:
                self.seasonal_indices.append(1.0)

        # 标准化季节性指数
        avg_index = np.mean(self.seasonal_indices)
        self.seasonal_indices = [idx / avg_index for idx in self.seasonal_indices]

        # 计算去季节化后的趋势
        self.avg_trend = np.mean(data) / avg_index if avg_index != 0 else np.mean(data)

    def predict(self, steps: int = 1, start_season: int = 0) -> List[float]:
        """
        预测未来 steps 期
        start_season: 预测起始季节索引
        """
        predictions = []

        for i in range(steps):
            season_idx = (start_season + i) % self.season_length
            seasonal_factor = self.seasonal_indices[season_idx]
            forecast = self.avg_trend * seasonal_factor
            predictions.append(max(0, forecast))

        return predictions


class MultiFactorPredictor:
    """
    多因素预测器
    综合考虑温度、降雨、施肥量、土壤pH等因素
    """

    def __init__(self):
        self.feature_weights = {
            'temperature': 0.25,      # 温度影响权重
            'rainfall': 0.20,         # 降雨影响权重
            'fertilizer': 0.20,       # 施肥量影响权重
            'soil_ph': 0.10,          # 土壤pH影响权重
            'sunshine': 0.15,         # 日照时长影响权重
            'historical_trend': 0.10  # 历史趋势权重
        }
        self.baseline_yield = 0
        self.coefficients = {}

    def fit(self, historical_yields: List[float],
            factors: Optional[List[Dict[str, float]]] = None) -> None:
        """
        拟合历史数据
        historical_yields: 历史产量列表
        factors: 历史因素数据列表（可选）
        """
        self.baseline_yield = np.mean(historical_yields) if historical_yields else 0

        if factors and len(factors) == len(historical_yields):
            # 简化的线性回归计算系数
            self._calculate_coefficients(historical_yields, factors)
        else:
            # 使用默认系数
            self.coefficients = {
                'temperature': 50,      # 每度温度影响
                'rainfall': 0.5,        # 每mm降雨影响
                'fertilizer': 2,        # 每kg施肥影响
                'soil_ph': -100,        # pH偏离最优值的影响
                'sunshine': 10          # 每小时日照影响
            }

    def _calculate_coefficients(self, yields: List[float], factors: List[Dict]) -> None:
        """计算各因素的回归系数（简化版）"""
        avg_yield = np.mean(yields)

        for factor_name in ['temperature', 'rainfall', 'fertilizer', 'soil_ph', 'sunshine']:
            values = [f.get(factor_name, 0) for f in factors]
            avg_value = np.mean(values)

            # 计算协方差和方差
            covariance = sum((yields[i] - avg_yield) * (values[i] - avg_value)
                           for i in range(len(yields)))
            variance = sum((v - avg_value) ** 2 for v in values)

            if variance != 0:
                self.coefficients[factor_name] = covariance / variance
            else:
                self.coefficients[factor_name] = 0

    def predict(self, current_factors: Dict[str, float],
                trend_adjustment: float = 0) -> Tuple[float, Dict[str, float]]:
        """
        基于当前因素预测产量
        返回: (预测值, 各因素贡献度)
        """
        contributions = {}

        # 温度贡献（最优温度范围 20-30°C）
        temp = current_factors.get('temperature', 25)
        temp_optimal = max(0, 1 - abs(temp - 25) / 15)  # 偏离25度越多，影响越大
        contributions['temperature'] = temp_optimal * self.feature_weights['temperature']

        # 降雨贡献（最优月降雨 100-200mm）
        rainfall = current_factors.get('rainfall', 150)
        rainfall_optimal = max(0, 1 - abs(rainfall - 150) / 150)
        contributions['rainfall'] = rainfall_optimal * self.feature_weights['rainfall']

        # 施肥贡献（假设合理施肥量）
        fertilizer = current_factors.get('fertilizer', 50)
        fertilizer_factor = min(1, fertilizer / 50) * self.feature_weights['fertilizer']
        contributions['fertilizer'] = fertilizer_factor

        # 土壤pH贡献（最优 6.0-7.0）
        ph = current_factors.get('soil_ph', 6.5)
        ph_optimal = max(0, 1 - abs(ph - 6.5) / 2)
        contributions['soil_ph'] = ph_optimal * self.feature_weights['soil_ph']

        # 日照贡献
        sunshine = current_factors.get('sunshine', 8)
        sunshine_factor = min(1, sunshine / 8) * self.feature_weights['sunshine']
        contributions['sunshine'] = sunshine_factor

        # 历史趋势
        contributions['historical_trend'] = (1 + trend_adjustment) * self.feature_weights['historical_trend']

        # 综合预测
        total_factor = sum(contributions.values())
        predicted = self.baseline_yield * total_factor * (1 + trend_adjustment * 0.1)

        return max(0, predicted), contributions


class EnsembleForecaster:
    """
    集成预测器
    组合多个预测模型，提高预测准确性
    """

    def __init__(self):
        self.ma_predictor = MovingAveragePredictor(window=3)
        self.es_predictor = ExponentialSmoothingPredictor(alpha=0.3, beta=0.1)
        self.seasonal_predictor = SeasonalPredictor(season_length=12)
        self.multi_factor_predictor = MultiFactorPredictor()

        # 各模型权重
        self.weights = {
            'moving_average': 0.15,
            'exponential_smoothing': 0.30,
            'seasonal': 0.35,
            'multi_factor': 0.20
        }

    def fit(self, historical_data: List[float],
            factors: Optional[List[Dict[str, float]]] = None) -> None:
        """拟合所有子模型"""
        self.ma_predictor.fit(historical_data)
        self.es_predictor.fit(historical_data)
        self.seasonal_predictor.fit(historical_data)
        self.multi_factor_predictor.fit(historical_data, factors)

    def predict(self, steps: int = 3,
                current_factors: Optional[Dict[str, float]] = None,
                current_season: int = 0) -> List[ForecastResult]:
        """
        集成预测
        steps: 预测期数
        current_factors: 当前环境因素
        current_season: 当前季节索引（0-11）
        """
        # 获取各模型预测
        ma_preds = self.ma_predictor.predict(steps)
        es_preds = self.es_predictor.predict(steps)
        seasonal_preds = self.seasonal_predictor.predict(steps, current_season)

        results = []

        for i in range(steps):
            # 加权平均
            weighted_sum = (
                ma_preds[i] * self.weights['moving_average'] +
                es_preds[i] * self.weights['exponential_smoothing'] +
                seasonal_preds[i] * self.weights['seasonal']
            )

            # 如果有环境因素，加入多因素预测
            if current_factors:
                trend_adj = (es_preds[i] - es_preds[0]) / es_preds[0] if es_preds[0] != 0 else 0
                mf_pred, contributions = self.multi_factor_predictor.predict(
                    current_factors, trend_adj
                )
                weighted_sum += mf_pred * self.weights['multi_factor']
            else:
                contributions = {}

            # 计算置信区间
            predictions = [ma_preds[i], es_preds[i], seasonal_preds[i]]
            std_dev = np.std(predictions)
            margin = 1.96 * std_dev  # 95% 置信区间

            confidence_interval = (
                max(0, weighted_sum - margin),
                weighted_sum + margin
            )

            # 判断趋势
            if i > 0:
                if weighted_sum > results[i-1].predicted_value * 1.02:
                    trend = 'up'
                elif weighted_sum < results[i-1].predicted_value * 0.98:
                    trend = 'down'
                else:
                    trend = 'stable'
            else:
                trend = 'stable'

            results.append(ForecastResult(
                predicted_value=round(weighted_sum, 2),
                confidence_interval=(round(confidence_interval[0], 2),
                                    round(confidence_interval[1], 2)),
                confidence_level=0.85,
                trend=trend,
                contributing_factors=contributions
            ))

        return results


# 模拟历史数据生成器
def generate_mock_historical_data(months: int = 24) -> List[Dict]:
    """生成模拟的历史产量数据"""
    np.random.seed(42)
    data = []

    base_yields = {
        '水稻': 2200,
        '玉米': 1800,
        '蔬菜': 800,
        '小麦': 1500
    }

    # 季节性因子（月份 -> 相对产量）
    seasonal_factors = {
        '水稻': [0, 0, 0.5, 0.8, 1.0, 1.2, 0, 0, 1.3, 1.5, 0.3, 0],
        '玉米': [0, 0, 0, 0, 0.6, 1.0, 1.3, 1.5, 0.8, 0, 0, 0],
        '蔬菜': [0.6, 0.7, 0.9, 1.0, 1.1, 0.8, 0.5, 0.4, 0.8, 1.0, 0.9, 0.7],
        '小麦': [0, 0, 0.5, 0.8, 1.2, 1.5, 0, 0, 0, 0, 0, 0]
    }

    crops = ['水稻', '玉米', '蔬菜']
    start_date = datetime(2024, 1, 1)

    for month in range(months):
        current_date = start_date + timedelta(days=30 * month)
        month_idx = current_date.month - 1

        for crop in crops:
            base = base_yields[crop]
            seasonal = seasonal_factors[crop][month_idx]

            if seasonal > 0:
                # 添加随机波动
                noise = np.random.normal(0, 0.1)
                yield_value = base * seasonal * (1 + noise)

                data.append({
                    'date': current_date.strftime('%Y-%m'),
                    'crop': crop,
                    'yield': max(0, round(yield_value, 0)),
                    'area': np.random.choice([3, 5, 8]),
                    'temperature': 20 + 10 * np.sin(month_idx * np.pi / 6) + np.random.normal(0, 2),
                    'rainfall': 100 + 50 * np.cos(month_idx * np.pi / 6) + np.random.normal(0, 20),
                    'fertilizer': 40 + np.random.normal(0, 10),
                    'soil_ph': 6.5 + np.random.normal(0, 0.3),
                    'sunshine': 6 + 3 * np.sin(month_idx * np.pi / 6) + np.random.normal(0, 1)
                })

    return data


# 服务接口
class ForecastService:
    """产量预测服务"""

    def __init__(self):
        self.forecaster = EnsembleForecaster()
        self.historical_data = []

    def load_historical_data(self, data: List[Dict]) -> None:
        """加载历史数据"""
        self.historical_data = data

    def forecast(self, crop: str = '水稻',
                 periods: int = 3,
                 current_factors: Optional[Dict[str, float]] = None) -> Dict:
        """
        执行产量预测

        Args:
            crop: 作物类型
            periods: 预测期数（月）
            current_factors: 当前环境因素

        Returns:
            预测结果字典
        """
        # 过滤特定作物的历史数据
        crop_data = [d for d in self.historical_data if d.get('crop') == crop]

        if not crop_data:
            # 使用模拟数据
            self.historical_data = generate_mock_historical_data()
            crop_data = [d for d in self.historical_data if d.get('crop') == crop]

        # 提取产量序列
        yields = [d['yield'] for d in sorted(crop_data, key=lambda x: x['date'])]

        # 提取环境因素
        factors = None
        if len(crop_data) > 0 and 'temperature' in crop_data[0]:
            factors = [{k: v for k, v in d.items()
                       if k in ['temperature', 'rainfall', 'fertilizer', 'soil_ph', 'sunshine']}
                      for d in crop_data]

        # 拟合模型
        self.forecaster.fit(yields, factors)

        # 获取当前月份作为季节索引
        current_season = datetime.now().month - 1

        # 执行预测
        results = self.forecaster.predict(
            steps=periods,
            current_factors=current_factors,
            current_season=current_season
        )

        # 构建返回结果
        forecast_data = []
        for i, result in enumerate(results):
            forecast_data.append({
                'period': i + 1,
                'predicted_yield': result.predicted_value,
                'confidence_lower': result.confidence_interval[0],
                'confidence_upper': result.confidence_interval[1],
                'confidence_level': result.confidence_level,
                'trend': result.trend,
                'factors': result.contributing_factors
            })

        # 汇总统计
        total_predicted = sum(r.predicted_value for r in results)
        avg_confidence = np.mean([r.confidence_level for r in results])

        return {
            'crop': crop,
            'forecast_periods': periods,
            'predictions': forecast_data,
            'summary': {
                'total_predicted_yield': round(total_predicted, 2),
                'average_monthly_yield': round(total_predicted / periods, 2),
                'overall_confidence': round(avg_confidence, 2),
                'prediction_range': (
                    round(sum(r.confidence_interval[0] for r in results), 2),
                    round(sum(r.confidence_interval[1] for r in results), 2)
                )
            },
            'algorithm_info': {
                'method': 'Ensemble (Moving Average + Exponential Smoothing + Seasonal + Multi-Factor)',
                'weights': self.forecaster.weights,
                'data_points': len(yields)
            }
        }


# 创建全局服务实例
forecast_service = ForecastService()
forecast_service.load_historical_data(generate_mock_historical_data())
