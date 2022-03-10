class Settings:
    def __init__(self):
        """
        Opening the settings.properties file here and saving
        its contents
        """
        file = open("settings.properties.txt","r")
        if file.mode == 'r':
            self._file = file

    def file_parse(self):
        """
        Establishing what types of repo we will use
        throughout the program
        :return:
        """
        repo_dict = {}
        f1 = self._file.readlines()
        self._file.close()
        for line in f1:
            tokens = line.strip().split("=",2)
            tokens[0] = tokens[0].strip()
            tokens[1] = tokens[1].strip()
            tokens[1] = tokens[1].strip('"')
            repo_dict[tokens[0]] = tokens[1].strip()
        return repo_dict

