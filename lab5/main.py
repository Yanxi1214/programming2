import timeit
import matplotlib.pyplot as plt


# ------------------------------
# Реализации функций вычисления факториала (четыре варианта)
# ------------------------------
def fact_recursive(n):
    """
    Рекурсивная реализация факториала без мемоизации
    :param n: Негативное целое число — основание факториала
    :return: Результат вычисления факториала n
    :raises ValueError: Если n является отрицательным числом
    """
    if n < 0:
        raise ValueError("n должно быть неотрицательным целым числом")
    # Базовый случай: 0! = 1, 1! = 1
    if n == 0 or n == 1:
        return 1
    # Рекурсивный вызов: n! = n * (n-1)!
    return n * fact_recursive(n - 1)


def fact_iterative(n):
    """
    Итеративная реализация факториала без мемоизации (через цикл for)
    :param n: Негативное целое число — основание факториала
    :return: Результат вычисления факториала n
    :raises ValueError: Если n является отрицательным числом
    """
    if n < 0:
        raise ValueError("n должно быть неотрицательным целым числом")
    result = 1
    # Умножение от 2 до n (1 не влияет на результат, поэтому пропускаем)
    for i in range(2, n + 1):
        result *= i
    return result


def fact_recursive_memo(n):
    """
    Рекурсивная реализация факториала с мемоизацией (пользовательский кэш)
    :param n: Негативное целое число — основание факториала
    :return: Результат вычисления факториала n
    :raises ValueError: Если n является отрицательным числом
    """
    # Внутренний словарь для кэширования уже вычисленных значений факториала
    memo = {0: 1, 1: 1}

    def helper(n):
        if n < 0:
            raise ValueError("n должно быть неотрицательным целым числом")
        # Сначала проверяем кэш: если значение есть, возвращаем его сразу
        if n in memo:
            return memo[n]
        # Если в кэше нет — вычисляем рекурсивно и сохраняем в кэш
        memo[n] = n * helper(n - 1)
        return memo[n]

    return helper(n)


# Глобальный кэш для итеративной реализации с мемоизацией (разделяется между вызовами)
fact_iter_memo_cache = {0: 1, 1: 1}


def fact_iterative_memo(n):
    """
    Итеративная реализация факториала с мемоизацией (на основе глобального кэша)
    :param n: Негативное целое число — основание факториала
    :return: Результат вычисления факториала n
    :raises ValueError: Если n является отрицательным числом
    """
    if n < 0:
        raise ValueError("n должно быть неотрицательным целым числом")
    # Если значение в кэше — возвращаем его
    if n in fact_iter_memo_cache:
        return fact_iter_memo_cache[n]
    # Если нет в кэше: начинаем умножение с максимального сохраненного значения (уменьшаем циклы)
    max_cached = max(fact_iter_memo_cache.keys())
    result = fact_iter_memo_cache[max_cached]
    for i in range(max_cached + 1, n + 1):
        result *= i
        fact_iter_memo_cache[i] = result  # Сохраняем в кэш
    return result


# ------------------------------
# Вспомогательные функции для бенчмаркинга
# ------------------------------
def get_average_time(func, n, runs=100):
    """
    Вычисление среднего времени выполнения функции при входном значении n
    :param func: Тестируемая функция
    :param n: Входной параметр для функции
    :param runs: Количество запусков (по умолчанию 100, чтобы снизить флуктуации системы)
    :return: Среднее время выполнения (в секундах)
    """
    # Формирование строки для выполнения через timeit (гарантируем независимость вызовов)
    stmt = f"{func.__name__}({n})"
    # Формирование строки для инициализации окружения (импортируем тестируемую функцию)
    setup = f"from __main__ import {func.__name__}"
    # Вычисление общего времени и возврат среднего значения
    total_time = timeit.timeit(stmt=stmt, setup=setup, number=runs)
    return total_time / runs


def generate_test_numbers(start=0, end=20, step=1):
    """
    Генерация фиксированного списка тестовых данных (чтобы данные не менялись между запусками)
    :param start: Начальное значение (по умолчанию 0)
    :param end: Конечное значение (по умолчанию 20, чтобы избежать переполнения стека рекурсии)
    :param step: Шаг (по умолчанию 1)
    :return: Список тестовых данных
    """
    return list(range(start, end + 1, step))


def run_benchmark(test_numbers, runs=100):
    """
    Запуск бенчмаркинга для всех функций вычисления факториала
    :param test_numbers: Список тестовых данных
    :param runs: Количество запусков для каждого тестового пункта
    :return: Словарь с результатами (ключ: имя функции, значение: список времен)
    """
    # Список тестируемых функций
    functions = [fact_recursive, fact_iterative, fact_recursive_memo, fact_iterative_memo]
    # Инициализация словаря для сохранения результатов
    results = {func.__name__: [] for func in functions}

    # Перебор каждого тестового пункта и вычисление среднего времени для всех функций
    print(f"Начало бенчмаркинга (каждое n запускается {runs} раз)...")
    for n in test_numbers:
        print(f"Тестируется n = {n:2d}", end="\r")
        for func in functions:
            avg_time = get_average_time(func, n, runs)
            results[func.__name__].append(avg_time)
    print("\nБенчмаркинг завершен!")
    return results


# ------------------------------
# Функция для построения графика производительности
# ------------------------------
def plot_performance(results, test_numbers, save_path="factorial_performance.png"):
    """
    Построение графика сравнения производительности (наглядно показывает зависимость времени от n)
    :param results: Словарь с результатами бенчмаркинга
    :param test_numbers: Список тестовых данных (ось X)
    :param save_path: Путь для сохранения изображения (по умолчанию в текущую директорию)
    """
    # Решение проблемы с отображением русских символов в matplotlib
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
    plt.rcParams['axes.unicode_minus'] = False

    # Определение стиля для каждой линии (чтобы отличать четыре реализации)
    line_styles = {
        "fact_recursive": {"color": "#e74c3c", "marker": "o", "label": "Рекурсия (без мемоизации)"},
        "fact_iterative": {"color": "#3498db", "marker": "s", "label": "Итерация (без мемоизации)"},
        "fact_recursive_memo": {"color": "#2ecc71", "marker": "^", "label": "Рекурсия (с мемоизацией)"},
        "fact_iterative_memo": {"color": "#f39c12", "marker": "D", "label": "Итерация (с мемоизацией)"}
    }

    # Создание фигуры и осей
    fig, ax = plt.subplots(figsize=(10, 6))

    # Построение кривой производительности для каждой функции
    for func_name, times in results.items():
        style = line_styles[func_name]
        ax.plot(
            test_numbers, times,
            color=style["color"],
            marker=style["marker"],
            label=style["label"],
            linewidth=2,
            markersize=6
        )

    # Настройка внешнего вида графика
    ax.set_xlabel("Входной параметр n (основание факториала)", fontsize=12)
    ax.set_ylabel("Среднее время выполнения (секунды)", fontsize=12)
    ax.set_title("Сравнение производительности четырех реализаций функции факториала", fontsize=14, fontweight="bold")
    ax.legend(fontsize=10, loc="upper left")
    ax.grid(True, alpha=0.3)  # Отображение сетки для удобства чтения данных

    # Сохранение изображения (высокое разрешение)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    print(f"\nГрафик производительности сохранен по пути: {save_path}")


# ------------------------------
# Точка входа в программу (запуск бенчмаркинга и построения графика)
# ------------------------------
if __name__ == "__main__":
    # 1. Конфигурация параметров теста
    TEST_RUNS = 100  # Количество запусков для каждого тестового пункта
    TEST_NUMBERS = generate_test_numbers(start=0, end=20)  # Фиксированные тестовые данные

    # 2. Запуск бенчмаркинга
    benchmark_results = run_benchmark(TEST_NUMBERS, TEST_RUNS)

    # 3. Вывод детальной таблицы результатов
    print("\n" + "="*80)
    print("Результаты бенчмаркинга (среднее время выполнения, единица: секунды)")
    print("="*80)
    # Вывод заголовков столбцов
    print(f"{'n':<6}", end="")
    for func_name in benchmark_results.keys():
        print(f"{func_name:<22}", end="")
    print("\n" + "-"*80)
    # Вывод данных для каждого тестового n
    for i, n in enumerate(TEST_NUMBERS):
        print(f"{n:<6}", end="")
        for func_name in benchmark_results.keys():
            time = benchmark_results[func_name][i]
            print(f"{time:<22.8f}", end="")  # Сохраняем 8 знаков после запятой для удобства сравнения
        print()

    # 4. Построение графика производительности
    plot_performance(benchmark_results, TEST_NUMBERS)
