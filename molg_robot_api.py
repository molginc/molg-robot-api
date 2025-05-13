#!/usr/bin/env python3
import logging
from typing import Optional

import numpy as np
import requests  # Added for HTTP requests

from micropsi_integration_sdk import JointPositionRobot, HardwareState

LOG = logging.getLogger(__name__)


class MolgStationAPI(JointPositionRobot):
    def __init__(self, **kwargs):
        """
        Initializes the MolgStationAPI instance.

        Args:
            **kwargs: Additional keyword arguments for configuration.
        """
        self.__host = kwargs.pop("host", "localhost")
        self.__port = kwargs.pop("port", 9305)
        super().__init__(**kwargs)
        self.__joint_positions = np.zeros(6)  # Assuming a 6-DOF robot
        self.__connected = False
        self.__ready_for_control = False
        self.__controlled = False
        LOG.debug("MolgStationAPI initialized with host=%s, port=%d", self.__host, self.__port)

    def _build_url(self, method_name: str) -> str:
        """
        Constructs the endpoint URL for a given method.

        Args:
            method_name (str): The name of the method.

        Returns:
            str: The constructed URL.
        """
        url = f"http://{self.__host}:{self.__port}/{method_name}"
        LOG.debug("Built URL: %s", url)
        return url

    def POST(self, method_name: str, headers: Optional[dict] = None, params: Optional[dict] = None, payload: Optional[dict] = None) -> Optional[dict]:
        """
        Performs a POST request to the specified method.

        Args:
            method_name (str): The API method name.
            headers (dict, optional): HTTP headers.
            params (dict, optional): Query parameters.
            payload (dict, optional): JSON payload.

        Returns:
            dict: The JSON response from the server.
        """
        url = self._build_url(method_name)
        LOG.debug("Performing POST request to %s with payload: %s", url, payload)
        response = requests.post(url, headers=headers, params=params, json=payload)
        response.raise_for_status()
        LOG.debug("POST response: %s", response.json())
        return response.json()

    def GET(self, method_name: str, headers: Optional[dict] = None, params: Optional[dict] = None) -> Optional[dict]:
        """
        Performs a GET request to the specified method.

        Args:
            method_name (str): The API method name.
            headers (dict, optional): HTTP headers.
            params (dict, optional): Query parameters.

        Returns:
            dict: The JSON response from the server.
        """
        url = self._build_url(method_name)
        LOG.debug("Performing GET request to %s", url)
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        LOG.debug("GET response: %s", response.json())
        return response.json()

    @staticmethod
    def get_supported_models() -> list:
        """
        Retrieves a list of supported robot models.

        Returns:
            list: A list of strings representing the names of supported robot models.
        """
        LOG.debug("Retrieving supported models.")
        models = ["MyRobot JointPosition"]
        LOG.debug("Supported models: %s", models)
        return models

    def get_joint_count(self) -> int:
        """
        Retrieves the number of joints in the robot.

        Returns:
            int: The number of joints.
        """
        LOG.debug("Getting joint count.")
        response = self.GET("get_joint_count")
        joint_count = response.get("joint_count", 0)
        LOG.debug("Joint count: %d", joint_count)
        return joint_count

    def get_joint_speed_limits(self) -> np.array:
        """
        Retrieves the speed limits for each joint.

        Returns:
            np.array: An array of speed limits.
        """
        LOG.debug("Getting joint speed limits.")
        response = self.GET("get_joint_speed_limits")
        limits = np.array(response.get("limits", [])) if response else np.array([])
        LOG.debug("Joint speed limits: %s", limits)
        return limits

    def get_joint_position_limits(self) -> np.array:
        """
        Retrieves the position limits for each joint.

        Returns:
            np.array: An array of position limits.
        """
        LOG.debug("Getting joint position limits.")
        response = self.GET("get_joint_position_limits")
        limits = np.array(response.get("limits", [])) if response else np.array([])
        LOG.debug("Joint position limits: %s", limits)
        return limits

    def connect(self) -> bool:
        """
        Connects to the robot.

        Returns:
            bool: True if connected, False otherwise.
        """
        LOG.debug("Connecting to the robot.")
        response = self.POST("connect")
        self.__connected = response.get("connected", False)
        LOG.debug("Connected: %s", self.__connected)
        return self.__connected

    def disconnect(self) -> None:
        """
        Disconnects from the robot.
        """
        LOG.debug("Disconnecting from the robot.")
        response = self.POST("disconnect")
        self.__connected = response.get("connected", False)
        LOG.debug("Disconnected: %s", not self.__connected)

    def prepare_for_control(self) -> None:
        """
        Prepares the robot for control.
        """
        LOG.debug("Preparing robot for control.")
        response = self.POST("prepare_for_control")
        self.__ready_for_control = response.get("ready_for_control", False)
        LOG.debug("Ready for control: %s", self.__ready_for_control)

    def is_ready_for_control(self) -> bool:
        """
        Checks if the robot is ready for control.

        Returns:
            bool: True if ready, False otherwise.
        """
        LOG.debug("Checking if robot is ready for control.")
        LOG.debug("Ready for control: %s", self.__ready_for_control)
        return self.__ready_for_control

    def take_control(self) -> None:
        """
        Takes control of the robot.
        """
        LOG.debug("Taking control of the robot.")
        response = self.POST("take_control")
        self.__controlled = response.get("controlled", False)
        LOG.debug("Control taken: %s", self.__controlled)

    def release_control(self) -> None:
        """
        Releases control of the robot.
        """
        LOG.debug("Releasing control of the robot.")
        self.POST("release_control")
        self.__controlled = False
        self.__ready_for_control = False
        LOG.debug("Control released.")

    def get_hardware_state(self) -> Optional[HardwareState]:
        """
        Retrieves the current hardware state of the robot.

        Returns:
            HardwareState: The hardware state object.
        """
        LOG.debug("Getting hardware state.")
        response = self.GET("get_hardware_state")
        if response:
            state = HardwareState(
                joint_positions=np.array(response.get("joint_positions", self.__joint_positions)),
            )
            LOG.debug("Hardware state: %s", state)
            return state
        LOG.debug("No hardware state available.")
        return None

    def clear_cached_hardware_state(self) -> None:
        """
        Clears the cached hardware state.
        """
        LOG.debug("Clearing cached hardware state.")
        self.POST("clear_cached_hardware_state")
        LOG.debug("Cached hardware state cleared.")

    def forward_kinematics(self, *, joint_positions: np.array) -> np.array:
        """
        Computes the forward kinematics for the given joint positions.

        Args:
            joint_positions (np.array): The joint positions.

        Returns:
            np.array: The end-effector pose.
        """
        LOG.debug("Computing forward kinematics.")
        response = self.POST("forward_kinematics", payload={"joint_positions": joint_positions.tolist()})
        pose = np.array(response.get("end_effector_pose")) if response else None
        LOG.debug("Forward kinematics result: %s", pose)
        return pose

    def inverse_kinematics(self, *, end_effector_pose: np.ndarray, joint_reference: Optional[np.ndarray]) -> Optional[np.ndarray]:
        """
        Computes the inverse kinematics for the given end-effector pose.

        Args:
            end_effector_pose (np.ndarray): The end-effector pose.
            joint_reference (np.ndarray, optional): A reference joint configuration.

        Returns:
            np.ndarray: The joint positions.
        """
        LOG.debug("Computing inverse kinematics.")
        response = self.POST("inverse_kinematics", payload={
            "end_effector_pose": end_effector_pose.tolist(),
            "joint_reference": joint_reference.tolist() if joint_reference is not None else None
        })
        joint_positions = np.array(response.get("joint_positions")) if response else None
        LOG.debug("Inverse kinematics result: %s", joint_positions)
        return joint_positions

    def are_joint_positions_safe(self, *, joint_positions: np.ndarray) -> bool:
        """
        Checks if the given joint positions are safe.

        Args:
            joint_positions (np.ndarray): The joint positions.

        Returns:
            bool: True if safe, False otherwise.
        """
        LOG.info("Checking if joint positions are safe.")
        response = self.POST("are_joint_positions_safe", payload={"joint_positions": joint_positions.tolist()})
        safe = response.get("safe", False)
        LOG.info("Joint positions safe: %s", safe)
        return safe

    def send_joint_positions(self, *, joint_positions: np.ndarray, step_count: int) -> None:
        """
        Sends joint positions to the robot.

        Args:
            joint_positions (np.ndarray): The joint positions.
            step_count (int): The number of steps for the movement.
        """
        LOG.debug("Sending joint positions.")
        self.POST("send_joint_positions", payload={
            "joint_positions": joint_positions.tolist(),
            "step_count": step_count
        })
        # self.__joint_positions = np.copy(joint_positions)
        LOG.debug("Joint positions sent: %s", joint_positions)

    def command_move(self, *, joint_positions: np.array) -> None:
        """
        Commands the robot to move to the specified joint positions.

        Args:
            joint_positions (np.array): The target joint positions.
        """
        LOG.info("Commanding robot to move.")
        self.POST("command_move", payload={"joint_positions": joint_positions.tolist()})
        # self.__joint_positions = np.copy(joint_positions)
        LOG.info("Move command executed with joint positions: %s", joint_positions)

    def command_stop(self) -> None:
        """
        Commands the robot to stop its current movement.
        """
        LOG.info("Commanding robot to stop.")
        self.POST("command_stop")
        LOG.info("Stop command executed.")
