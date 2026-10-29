from datetime import datetime
import ast

class Log:

    def write(self, content_line: dict):
        """
            Writes a line of content to the log file
        """

        status_line: str = content_line["Status"]

        current_time: str = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        output: dict = {}
        output.update({"Zeit": current_time})
        output.update(content_line)

        with open('history.log', encoding="utf-8") as log:

            last_line: str = list(log)[-1].strip()
            log_dict: dict = ast.literal_eval(last_line)

        status: str = log_dict['Status']
        print(f"Log last Line status: {status}")

        if status != status_line:
            with open('history.log', mode='a') as log2:
                log2.write(f"\n{output}")

                print(output)
