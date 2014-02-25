__author__ = 'wei'

from protobuf import *


class BaseTemplate:
    def __init__(self):
        self.appKey = ""
        self.appId = ""
        self.pushInfo = None

    def getTransparent(self):
        transparent = gt_req_pb2.Transparent()
        transparent.id = ""
        transparent.action = "pushmessage"
        transparent.taskId = ""
        transparent.appKey = self.appKey
        transparent.appId = self.appId
        transparent.messageId = ""
        transparent.pushInfo.CopyFrom(self.getPushInfo())
        actionChains = self.getActionChains()
        for actionChain in actionChains:
            tmp = transparent.actionChain.add()
            tmp.CopyFrom(actionChain)
        return transparent

    def getActionChains(self):
        return []

    def getPushInfo(self):
        if self.pushInfo is None:
            self.pushInfo = gt_req_pb2.PushInfo()
            self.pushInfo.message = ""
            self.pushInfo.actionKey = ""
            self.pushInfo.sound = ""
            self.pushInfo.badge = ""
        return self.pushInfo

    def setPushInfo(self, actionLocKey, badge, message, sound, payload, locKey, locArgs, launchImage):
        self.pushInfo = gt_req_pb2.PushInfo()
        self.pushInfo.actionLocKey = actionLocKey
        self.pushInfo.badge = str(badge)
        self.pushInfo.message = message
        self.pushInfo.sound = sound
        self.pushInfo.payload = payload
        self.pushInfo.locKey = locKey
        self.pushInfo.locArgs = locArgs
        self.pushInfo.launchImage = launchImage


