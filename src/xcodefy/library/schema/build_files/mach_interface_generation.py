from xcodefy.library.serialization.codable_str_enum import CodableStrEnum


class MachInterfaceGeneration(CodableStrEnum):
    CLIENT = "client"
    SERVER = "server"
    BOTH = "both"
