from PyQt6.QtWidgets import QMessageBox

import sys
import traceback


def display_message(message: str, title="Сообщение"):
    msgBox = QMessageBox()
    msgBox.setText(title)
    msgBox.setInformativeText(message)
    msgBox.setStandardButtons(QMessageBox.StandardButton.Close)
    ret = msgBox.exec()


def display_detailed_error_message(message: str, ex: Exception):
    msgBox = QMessageBox()
    msgBox.setText("Ошибка.")
    msgBox.setInformativeText(message)

    # Get current system exception
    ex_type, ex_value, ex_traceback = sys.exc_info()

    # Extract unformatter stack traces as tuples
    trace_back = traceback.extract_tb(ex_traceback)

    # Format stacktrace
    stack_trace = list()

    for trace in trace_back:
        stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

    # print("Exception type : %s " % ex_type.__name__)
    # print("Exception message : %s" %ex_value)
    # print("Stack trace : %s" %stack_trace)

    info = "{}".format(stack_trace)

    msgBox.setDetailedText(info)
    msgBox.setStandardButtons(QMessageBox.StandardButton.Close)
    ret = msgBox.exec()

