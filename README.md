# Radiant

![Banner](https://user-images.githubusercontent.com/79613445/210191579-2c2f9967-d397-4ef7-8330-bbb17eed17ea.png)

Radiant is a Addon that helps manage your lights in your scene through the side panel. There are also a few other feature provided for lighting needs in Radiant

	This Addon Only works for Blender 3.0 and Above, It will crash your blender if you use Raymesh in Blender 2.9x and below
	
[RadiantDemo.webm](https://user-images.githubusercontent.com/79613445/210191585-fed39e22-a5c7-4a76-957b-9c6537e01097.webm)

	
## Raymesh

Raymesh is Fake "Light Ray / Glow" that is Geometry and Shader Based, It Attempt to Emulate the Volumetric Look

![Raymesh](https://user-images.githubusercontent.com/79613445/210191597-350c2814-2db9-44b9-b9fd-11c6a87c60e9.png)


|Raymesh Only|No Raymesh|With Raymesh|
|--|--|--|
|![OnlyRaymesh](https://user-images.githubusercontent.com/79613445/210191608-5a94de7b-ffa9-408d-a949-ecbc6e7a8577.png) |![NoRaymesh](https://user-images.githubusercontent.com/79613445/210191619-f8b8babe-2e0b-452b-8aa0-ab25b257f197.png) |![WithRaymesh](https://user-images.githubusercontent.com/79613445/210191625-09423b17-e2a4-45f4-8eb3-13e0afaebc6a.png)|

It Produces Less Noise, Doesnt Flicker, and Works Best in Eevee, this can be useful for Stylized Lighting


### Raymesh Variations

If the Raymesh use Light as Driver, it means the Custom Property in Raymesh Object is driven by Custom Property in the Light data


|Point Raymesh|Spot Raymesh|Area Raymesh|
|--|--|--|
|![PointRaymesh](https://user-images.githubusercontent.com/79613445/210191637-d485439d-57f4-4ca2-a523-3b5bbe971618.png)|![SpotRaymesh](https://user-images.githubusercontent.com/79613445/210191640-ca693d1f-0eb7-409b-a090-cad23143bdfc.png)|![AreaRaymesh](https://user-images.githubusercontent.com/79613445/210191645-e5dbe08b-3e39-4f8e-8eb6-b8160dccb7d4.png)|


	Technical Information:
	
	Raymesh Geometry is made using Geometry Nodes, and using Material Shader to Achieve the Glowly Looks
	
	The Geometry and Shader is Driven by Custom Properties in the Raymesh Object's Custom Properties.
	
	
	If the Raymesh use Light as Driver, it means the Custom Property in Raymesh Object is driven by Custom Property in the Light data


---

	Notes
	
	While it is Compatible with Cycles, because it heavily relies on transparency to work, it might not look as good in cycles, and you might need to increase your transparent light bounce for it to work, which could increase in render time


| Point | Spot | Area |
| -- | -- | -- |
| [PointGlow.webm](https://user-images.githubusercontent.com/79613445/210192140-b8a05176-f411-4d4f-aa62-6c984535882e.webm) | [SpotGlow.webm](https://user-images.githubusercontent.com/79613445/210192145-1426b612-c764-41e9-ac78-795b8397876c.webm) | [AreaGlow.webm](https://user-images.githubusercontent.com/79613445/210192152-8ef7b7c1-47ba-4239-8b7f-9acffc5f9879.webm) |


## Light Panel

List the Light in Your Scene to the Side Panel and access multiple light at once. It gives you a Filterable Overview of the Light in Your Scene.

![LightPanel](https://user-images.githubusercontent.com/79613445/210191730-da9397ad-cab5-42cc-9f96-08e1ebd16fa2.png)

### Why Not Outliner?

Outliner can be cluttered sometimes, especially on more complex scene, this Panel helps you focus on the Light and filter out other object types.

### Light Panel Buttons

With each Light Listed, there are some operation you can do to each lights


![DefaultLightPanelHeader](https://user-images.githubusercontent.com/79613445/210191722-75dc6fdb-023e-4512-9a3d-e54135cee010.png)

You Can Turn the Buttons / Icons you want on or off under the Icon Expose Subpanel,

Below Example of All the Icons Turned On

![FullLightPanelHeader](https://user-images.githubusercontent.com/79613445/210191726-555e0f61-76e9-4e25-8f43-2a86022c2dc6.png)


Most of the Icon are Turned Off by default


| Buttons / Icons | Default | Description |
| -- | -- | -- |
| Pin Light | Off | Pin the light so that it always stays in list |
| Solo Light| Off |  	Hide All Light Except this (Shift Click to Unhide Lights) |
| Select Light | **On** | Select the Light (Shift Click to Select Multiple) |
| Find Light | **On** |  Find and Frame your camera to the Light |
| Move Light | Off | Activate Move Operator on this Light |
| Rotate Light | Off | Active Trackball / Rotate Operator on this Light |
| Aim Light | Off | Aim the Light to Object, Selected Objects, or Cursor |
| Name | **Always On** | Name of the Light |
| Tags | Off | Tags of the Light to be use for filtering |
| Light Type | Off | Set the Type of the Light |
| Light Color | Off | Set the Color of the Light |
| Disable / Lock Selection | Off | Make Light Unselectable |
| Hide Children | **On** | Hide The Lights Children, Useful for Hiding Raymesh (Only Show if Light Have Children) |
| Hide Viewport | **On** | Hide The Lights Children, Useful for Hiding Raymesh (Only Show if Light Have Children) |
| Hide Render | **On** | Disable Render for this Light |
| Duplicate Light | Off | Duplicate This Light and Active Move Operator |
| Remove Light | **On** |  	Remove this Light |

### Light Properties

For Each light in the Panel, You can Expand And Edit the Light's Properties, Such as Power, Shadow Soft Size, Factor, and more

![LightProperties](https://user-images.githubusercontent.com/79613445/210191738-052e0327-38a3-441b-880d-5f5233702263.png)


### Light Temperature

Control Light Color Using Kelvin Temperature

[LightTemperature.webm](https://user-images.githubusercontent.com/79613445/210191713-7d4c17dc-6011-4b06-8b1d-b76112fa624c.webm)


	IMPORTANT:
	The Temperature only changes the color on the Light when you drag the slider, Which means it will not work if you Keyframe the Temperature
	
	This Does not Use the Blackbody Node but Instead Setting the Light Color Directly



## Light Tags & List Filter

You Can Tag the Light so that You can Filter Them

### Light Tags

Light Tag is something you can add to a light to be used in the List Filter, Useful for Categorizing Your Lights

[LightTags.webm](https://user-images.githubusercontent.com/79613445/210191830-24528efe-42b1-4921-acc0-94d25d186d32.webm)


### Light List Filter

| Item | Description |
| -- | -- |
| All |	List All the Lights In the Scene |
| Selected |	List Only Selected Lights |
| Active |	Show Only Active Light |
| Collection |	Show Light in Collection |
| Tags |	Filter Light by Tags |
| Pinned |	Only Show Pinned Lights |
| Type 	| Filter Light Base on the Type of the Lights |



## Radiant Tools

Some More Minor tools that can be useful in some situation

![RadiantTools](https://user-images.githubusercontent.com/79613445/210191743-cb067de2-20d4-4fb8-9305-a26edc3f6cf0.png)


### Create Mesh From Area Lights

Create Mesh Plane From Area Light, Useful if you want to have a Emission Plane for your Area Lights

[AreahLightFromMesh.webm](https://user-images.githubusercontent.com/79613445/210192070-6e5bd42b-3eae-4d05-98ed-8f3377be5dba.webm)


### Add Shadow Catcher

Add A Premade Shadow Catcher Plane from Shift-A Add Panel

[ShadowCatcher.webm](https://user-images.githubusercontent.com/79613445/210192096-b920f032-3caa-4c77-ae36-b8efaa67a06a.webm)


If the Shadow Catcher Appears Black in Eevee, Try Increase the Strength of your Lights


### Add Volume Cube

Add A Simple Premade Cube with Principled Volume Node Material Applied

[VolumeCube.webm](https://user-images.githubusercontent.com/79613445/210192118-e2938bff-564a-4b66-b7d8-fe2617ec878e.webm)


	This is an Extremely Simple Setup, this feature is just here to save a few clicks
