from functions.get_files_info import get_files_info

def test_get_files_info():
    print(get_files_info("calculator", "."))
    print(get_files_info("calculator", "pkg"))
    print(get_files_info("calculator", "/bin"))
    print(get_files_info("calculator", "../"))
    
test_get_files_info()