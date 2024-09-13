from abc import ABC, abstractmethod
from datetime import datetime
from io import BytesIO
from typing import Dict, Generic, List, Optional, TypeVar, Union

from .request_information import RequestInformation
from .serialization import Parsable, ParsableFactory, SerializationWriterFactory
from .store import BackingStoreFactory

ResponseType = TypeVar("ResponseType")
ModelType = TypeVar("ModelType", bound=Parsable)
RequestType = TypeVar("RequestType")


class RequestAdapter(ABC, Generic[RequestType]):
    """Service responsible for translating abstract Request Info into concrete native HTTP requests.
    """
    # The base url for every request.
    base_url = str()

    @abstractmethod
    def get_serialization_writer_factory(self) -> SerializationWriterFactory:
        """Gets the serialization writer factory currently in use for the HTTP core service.

        Returns:
            SerializationWriterFactory: the serialization writer factory currently in use for the
            HTTP core service.
        """
        pass

    @abstractmethod
    async def send_async(
        self, request_info: RequestInformation, parsable_factory: ParsableFactory[ModelType],
        error_map: Optional[Dict[str, ParsableFactory]]
    ) -> Optional[ModelType]:
        """Excutes the HTTP request specified by the given RequestInformation and returns the
        deserialized response model.

        Args:
            request_info (RequestInformation): the request info to execute.
            parsable_factory (ParsableFactory): the class of response model to
                deserialize the response into.
            error_map (Optional[Dict[str, ParsableFactory]]): the error dict to use in case
            of a failed request.

        Returns:
            ModelType: the deserialized response model.
        """
        pass

    @abstractmethod
    async def send_collection_async(
        self,
        request_info: RequestInformation,
        parsable_factory: ParsableFactory,
        error_map: Optional[Dict[str, ParsableFactory]],
    ) -> Optional[List[ModelType]]:
        """Excutes the HTTP request specified by the given RequestInformation and returns the
        deserialized response model collection.

        Args:
            request_info (RequestInformation): the request info to execute.
            parsable_factory (ParsableFactory): the class of response model to
                deserialize the response into.
            error_map (Optional[Dict[str, ParsableFactory]]): the error dict to use in
            case of a failed request.

        Returns:
            ModelType: the deserialized response model collection.
        """
        pass

    @abstractmethod
    async def send_collection_of_primitive_async(
        self,
        request_info: RequestInformation,
        response_type: ResponseType,
        error_map: Optional[Dict[str, ParsableFactory]],
    ) -> Optional[List[ResponseType]]:
        """Excutes the HTTP request specified by the given RequestInformation and returns the
        deserialized response model collection.

        Args:
            request_info (RequestInformation): the request info to execute.
            response_type (ResponseType): the class of the response model to deserialize the
            response into.
            error_map (Optional[Dict[str, ParsableFactory]]): the error dict to use in
            case of a failed request.

        Returns:
            Optional[List[ModelType]]: The deserialized response model collection.
        """
        pass

    @abstractmethod
    async def send_primitive_async(
        self, request_info: RequestInformation, response_type: str,
        error_map: Optional[Dict[str, ParsableFactory]]
    ) -> Optional[ResponseType]:
        """Excutes the HTTP request specified by the given RequestInformation and returns the
        deserialized primitive response model.

        Args:
            request_info (RequestInformation): the request info to execute.
            response_type (str): the class name of the response model to deserialize the
            response into.
            error_map (Optional[Dict[str, ParsableFactory]]): the error dict to use in
            case of a failed request.

        Returns:
            ResponseType: the deserialized primitive response model.
        """
        pass

    @abstractmethod
    async def send_no_response_content_async(
        self, request_info: RequestInformation, error_map: Optional[Dict[str, ParsableFactory]]
    ) -> None:
        """Excutes the HTTP request specified by the given RequestInformation and returns the
        deserialized primitive response model.

        Args:
            request_info (RequestInformation):the request info to execute.
            error_map (Optional[Dict[str, ParsableFactory]]): the error dict to use in
            case of a failed request.
        """
        pass

    @abstractmethod
    def enable_backing_store(self, backing_store_factory: Optional[BackingStoreFactory]) -> None:
        """Enables the backing store proxies for the SerializationWriters and ParseNodes in use.

        Args:
            backing_store_factory (Optional[BackingStoreFactory]): the backing store factory to use.
        """
        pass

    @abstractmethod
    async def convert_to_native_async(self, request_info: RequestInformation) -> RequestType:
        """Translates the request information object into a native HTTP client request object.

        Args:
            request_info (RequestInformation): request information object to be converted.

        Returns:
            RequestType: the natively typed HTTP request of the client.
        """
        pass
