from fastapi import Query


class ReportQueryParams:
    """Класс для параметров запроса отчета"""
    def __init__(
            self,
            report_format: str = Query(..., description="Доступные форматы отчета: csv или xlsx")
    ) -> None:
        """
        Описывает query параметры

        Parameters:
            report_format: формат отчета
        """
        self.report_format = report_format
