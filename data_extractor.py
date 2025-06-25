# Here we read the each segment of the customer profile from /data for a given customerid
import pandas as pd
import os
from config_loader import load_config
import logging



class data_loader:
    """
    A class to handle loading customer profile data.
    """
    

    def __init__(self, customer_id):
        self.customer_id = customer_id
    
    def get_profile_sources(self):
        """
        Returns a list of sources for the customer profile segments.
        """
        config = load_config()
        profile_sources = config.get('customer_profile_segments')
        return profile_sources
    
    def load_demographics(self):
        """
        Loads the demographics data for the customer.
        """
        sources = self.get_profile_sources()
        demographics_path = os.path.join('data', sources['demographics'])
        if not os.path.exists(demographics_path):
            raise FileNotFoundError(f"Demographics data not found for customer {self.customer_id}")
        
        data =  pd.read_csv(demographics_path)
        # filter by the customer_id
        customer_demographics = data[data['customer_id'] == self.customer_id]
        return customer_demographics.to_dict(orient = "records")[0]
    
    def load_asset_allocation(self):
        """
        Loads the asset allocation data for the customer.
        """
        sources = self.get_profile_sources()
        asset_allocation_path = os.path.join('data', sources['asset_allocation'])
        if not os.path.exists(asset_allocation_path):
            raise FileNotFoundError(f"Asset allocation data not found for customer {self.customer_id}")
        
        data = pd.read_csv(asset_allocation_path)
        # filter by the customer_id
        customer_asset_allocation = data[data['customer_id'] == self.customer_id]
        return customer_asset_allocation.to_dict(orient = "records")[0]
    
    def load_trade_history(self):
        """
        Loads the trade history data for the customer.
        """
        sources = self.get_profile_sources()
        trade_history_path = os.path.join('data', sources['trade_history'])
        if not os.path.exists(trade_history_path):
            raise FileNotFoundError(f"Trade history data not found for customer {self.customer_id}")
        
        data = pd.read_csv(trade_history_path)
        # filter by the customer_id
        customer_trade_history = data[data['customer_id'] == self.customer_id]
        return customer_trade_history.to_dict(orient = "records")[0]
    
    def load_positions(self):
        """
        Loads the open positions data for the customer.
        """
        sources = self.get_profile_sources()
        positions_path = os.path.join('data', sources['positions'])
        if not os.path.exists(positions_path):
            raise FileNotFoundError(f"Positions data not found for customer {self.customer_id}")
        
        data = pd.read_csv(positions_path)
        # filter by the customer_id
        customer_positions = data[data['customer_id'] == self.customer_id]
        return customer_positions.to_dict(orient = "records")[0]

    def load_interactions(self):
        """
        Loads the interactions data for the customer.
        """
        sources = self.get_profile_sources()
        interactions_path = os.path.join('data', sources['interactions'])
        if not os.path.exists(interactions_path):
            raise FileNotFoundError(f"Interactions data not found for customer {self.customer_id}")
        
        data = pd.read_csv(interactions_path)
        # filter by the customer_id
        customer_interactions = data[data['customer_id'] == self.customer_id]
        return customer_interactions.to_dict(orient = "records")[0]    

    def load_portfolio(self):
        """
        Loads the complete portfolio structure for the customer.
        """
        sources = self.get_profile_sources()
        portfolio_path = os.path.join('data', sources['portfolio'])
        if not os.path.exists(portfolio_path):
            raise FileNotFoundError(f"portfolio data not found for customer {self.customer_id}")
        
        data = pd.read_csv(portfolio_path)
        # filter by the customer_id
        customer_portfolio = data[data['customer_id'] == self.customer_id]
        return customer_portfolio.to_dict(orient = "records")[0]

    def set_consolidated_investor_profile(self):
        """
        Consolidates all customer profile segments into a single dictionary.
        """
        profile = {
            'demographics': self.load_demographics(),
            'asset_allocation': self.load_asset_allocation(),
            'trade_history': self.load_trade_history(),
            'positions': self.load_positions(),
            'interactions': self.load_interactions(),
            'portfolio': self.load_portfolio()
        }
        return profile      


# Example usage
def get_consolidated_investor_profile(customer_id):
    """
    Function to get the consolidated investor profile for a given customer ID.
    
    Args:
        customer_id (str): The ID of the customer.
        
    Returns:
        dict: The consolidated investor profile data.
    """
    loader = data_loader(customer_id)
    logging.info(f"Loading consolidated investor profile for customer {customer_id}")
    return loader.set_consolidated_investor_profile()


    
