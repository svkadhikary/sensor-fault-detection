from dataclasses import dataclass




@dataclass
class DataIngestionArtifact:
    train_file_path:str
    test_file_path:str


@dataclass
class DataValidationArtifact:
    report_file_path:str
    train_file_path:str
    test_file_path:str
    status:bool


@dataclass
class DataTransformationArtifact:
    transformer_object_path:str 
    transformed_train_path:str 
    transformed_test_path:str 
    target_encoder_path:str


@dataclass
class ModelTrainerArtifact:
    model_file_path:str
    f1_train_score:float
    f1_test_score:float


@dataclass
class ModelEvaluationArtifact:
    improved_model_accuracy:float
    is_model_accepted:bool

@dataclass
class ModelPusherArtifact:
    pusher_model_dir:str 
    saved_model_dir:str

