from dataclasses import dataclass


@dataclass
class Config:
    save_additional_data: bool = True # if set to false, doesn't save depiction etc
    ignore_errors: bool = True # if set to false, crashes on deb save error
    recheck_paid_packages: bool = False # TODO: unimplemented
    print_progress: bool = True
    print_paid_packages: bool = True # TODO: unimplemented
    print_deb_fails: bool = True  # TODO: unimplemented
    print_additional_fails: bool = True #TODO: unimplemented


    # def __init__(self, 
    #              save_additional_data: bool = True,

    #              ):
    #     self.save_additional_data = save_additional_data
        