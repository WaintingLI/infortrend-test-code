"""
測試Cliclkhouse是否安裝正常
"""
import sys
import traceback
import clickhouse_connect




if __name__ == "__main__":
    client = clickhouse_connect.get_client(
        host='172.24.128.220',
        port=8123,
        username='admin',
        password='admin123',
        connect_timeout=30
        )
    client.command("CREATE DATABASE IF NOT EXISTS testconnect")
    #print(client.command("SHOW DATABASES"))
    client.close()
    try:
        client = clickhouse_connect.get_client(
            host='172.24.128.220',
            port=8123,
            username='admin',
            password='admin123',
            database='testconnect1')
        #print(type(client.command("SHOW DATABASES")))
        #print()
        client.close()
    except Exception  as e:
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()

        # Extract unformatter stack traces as tuples
        trace_back = traceback.extract_tb(ex_traceback)

        # Format stacktrace
        stack_trace = list()

        for trace in trace_back:
            stack_trace.append("File : %s ,\nLine : %d,\nFunc.Name : %s,\nMessage : %s\n" % (trace[0], trace[1], trace[2], trace[3]))
        print("Exception type : %s " % ex_type.__name__)
        print("Exception message : %s" %ex_value)
        #print("Stack trace : %s" %stack_trace)
        for item in stack_trace:
            print(item)
        
