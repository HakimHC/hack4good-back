"use client"

interface UserInputApi {
  name: string;
  height: string;
  weight: string;
  age: string;
  sex: string;
  physical_activity: string;
  vegan_or_vegetarian: string;
  allergies: string;
}


import { useForm } from "react-hook-form";
import {
	Form,
	FormControl,
	FormDescription,
	FormField,
	FormItem,
	FormLabel,
	FormMessage,
	useFormField
} from "./react-form"

import { z } from "zod"
import { zodResolver } from "@hookform/resolvers/zod";
 
const formSchema = z.object({
  username: z.string().min(2).max(50),
})

export const UserForm = () => {
	// 1. Define your form.
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      username: "",
    },
  })
 
  // 2. Define a submit handler.
  function onSubmit(values: z.infer<typeof formSchema>) {
    // Do something with the form values.
    // ✅ This will be type-safe and validated.
    console.log(values)
  }
	
	return (
		<div>
			<Form {...form}>
			<form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">

				<FormField
					control={form.control}
					name="username"
					render={({ field }) => (
						<FormItem>
						<FormLabel>Hello world</FormLabel>
						<FormControl>
							<input type="text"  placeholder="Hello Word..." {...field} />
						</FormControl>
						<FormDescription />
						<FormMessage />
					</FormItem>
				)}
				/>
				</form>
			</Form>
	</div>
	)
}