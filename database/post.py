import re
from datetime import datetime
from typing import Any, Optional


class Post(object):

    __CLASS_METHOD_REGEX = r'^(?:(?P<class_name>.*)::)?(?P<method_name>\w+(?:<.*>)?\(.*\))$'

    def __init__(self, handler_factory: TableHandlerFactory):
        self.__table_handler = handler_factory

    def is_record_before(self, commit_hash: str) -> bool:
        return self.__table_handler.for_commits.is_hash_exist(commit_hash)

    def record_git_commit(self, commit_hash: str, commit_date: datetime) -> Any:
        result = self.__table_handler.for_commits.insert_new_commit(commit_hash, commit_date)
        self.__table_handler.for_commits.flash()
        return result

    def record_file_relocate(self, old_path: str, new_path: str) -> None:
        id_pairs = self.__table_handler.for_methods.find_crash_rows_of_relocate(old_path, new_path)
        for old_id, new_id in id_pairs:
            self.__table_handler.for_changes.update_target_method(new_id, old_id)
            self.__table_handler.for_methods.delete_methods_by_id(new_id)
        self.__table_handler.for_methods.update_path(old_path, new_path)
        return None

    def record_rename_class(self, path: str, old_class: str, new_class: str) -> None:
        methods_table = self.__table_handler.for_methods
        change_table = self.__table_handler.for_changes
        id_pairs = methods_table.find_crash_rows_of_class_rename(path, old_class, new_class)
        for old_id, new_id in id_pairs:
            change_table.update_target_method(new_id, old_id)
            methods_table.delete_methods_by_id(new_id)
        self.__table_handler.for_methods.update_class(path, old_class, new_class)
        return None

    def record_rename_method(self, method_id: int, new_name: str, commit_hash: str) -> None:
        match_names = re.match(self.__CLASS_METHOD_REGEX, new_name).groupdict()
        method_name = match_names['method_name'].replace('( ', '(', 1).replace(' ,', ',')
        methods_table = self.__table_handler.for_methods
        change_table = self.__table_handler.for_changes
        id_pairs = methods_table.find_crash_rows_of_method_rename(method_id, method_name)
        for old_id, new_id in id_pairs:
            change_table.update_target_method(new_id, old_id)
            methods_table.delete_methods_by_id(new_id)
        change_table.insert_new_change("RENAME", method_id, commit_hash)
        methods_table.update_name(method_id, method_name)
        return None

    def get_method_id(self, method_name: str, class_name: Optional[str], path: str) -> int:
        match_names = re.match(self.__CLASS_METHOD_REGEX, method_name).groupdict()
        method_name = match_names['method_name'].replace('( ', '(', 1).replace(' ,', ',')
        if class_name is None: class_name = '' # The class name is Null because of the PyDriller
        return self.__table_handler.for_methods.select_method_id(method_name, class_name, path)

    def record_remove_method(self, method_id: int) -> None:
        self.__table_handler.for_methods.delete_methods_by_id(method_id)
        self.__table_handler.for_changes.delete_changes_of(method_id)
        return None

    def record_add_method(self, method_id: int, commit_hash: str) -> int:
        change_table = self.__table_handler.for_changes
        return change_table.insert_new_change('ADD', method_id, commit_hash)

    def record_modify_method(self, method_id: int, commit_hash: str) -> int:
        change_table = self.__table_handler.for_changes
        return change_table.insert_new_change('MODIFY', method_id, commit_hash)