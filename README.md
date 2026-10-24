# Расчет оплаты по ступенчатому тарифу

Тема 2: Расчет оплаты за коммунальные услуги (электроэнергия) по ступенчатому тарифу. Базовый объем считается по одной ставке, превышение лимита - по повышенной.

## Запуск

Стандартный запуск:
```bash
python src/main.py
```

Запуск со своими файлами:
```bash
python src/main.py data/input_standard.json data/output_report.json
```

Запуск тестов:
```bash
python tests/test_runner.py
```

## Схемы и документация

* Входные данные: `data/input_standard.json`
* Общая схема программы: [docs/flowcharts/main_scenario.png](docs/flowcharts/main_scenario.png)
* Схема алгоритма: [docs/flowcharts/tariff_algorithm.png](docs/flowcharts/tariff_algorithm.png)
* Описание алгоритма: [docs/algorithms.md](docs/algorithms.md)
* Тест-кейсы: [docs/test-cases.md](docs/test-cases.md)
