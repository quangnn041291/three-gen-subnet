import copy
import typing

import bittensor as bt

from storage_subnet.models import StoredData
from storage_subnet.protocol import StoreUser


class Keeper:
    def __init__(self, config: bt.config) -> None:
        self.config: bt.config = copy.deepcopy(config)

        # TODO: replace with bt.subtensor(config=self.config) once SN21 firewall issue is resolved.
        self.subtensor = bt.subtensor(network="test")

        self.metagraph = bt.metagraph(netuid=self.config.storage.netuid, network=self.subtensor.network, sync=False)
        self.metagraph.sync(subtensor=self.subtensor)

        self.wallet = bt.wallet(
            name=config.storage.wallet.name, hotkey=config.storage.wallet.hotkey, path=config.storage.wallet.path
        )

        # TODO: add periodic resync in case of validator migration

        # TODO: add saving queue to save one object at a time

        # TODO: save all CIDs to the file

        # TODO: configure storage subnet validator uid? hotkey

    async def store(self, data: StoredData) -> None:
        # TODO: proper ttl
        ttl: int = 60 * 60 * 24

        synapse = StoreUser(
            encrypted_data=data.to_base64(),
            encryption_payload="{}",
            ttl=ttl,
        )

        dendrite = bt.dendrite(wallet=self.wallet)

        timeout = 120
        cid = None
        for attempt in range(3):
            response = typing.cast(
                StoreUser,
                await dendrite.call(
                    target_axon=self.metagraph.axons[7], synapse=synapse, timeout=timeout, deserialize=False
                ),
            )
            if response.axon.status_code == 200:
                bt.logging.info(f"Saved successfully. CID: {response.data_hash}")
                cid = response.data_hash
                break

            bt.logging.debug(
                f"Attempt #{attempt}. Saving to SN21 failed with: "
                f"{response.axon.status_message}({response.axon.status_code})"
            )
            timeout += 120
        else:
            bt.logging.error("Failed to save generated assets to SN21")

        if cid is not None:
            bt.logging.info(f"Data save to the storage subnet. CID: {cid}")
